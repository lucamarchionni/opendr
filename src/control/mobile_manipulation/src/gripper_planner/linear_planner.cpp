#include <gripper_planner/linear_planner.h>

LinearPlanner::LinearPlanner(const std::vector<double> &gripper_goal_wrist, const std::vector<double> &initial_gripper_tf,
                             const std::vector<double> &base_goal, const std::vector<double> &initial_base_tf,
                             double success_thres_dist, double success_thres_rot, const double &min_planner_velocity,
                             const double &max_planner_velocity, const double &slow_down_factor, const double &head_start,
                             const double &time_step_train, const bool &is_analytic_env) :
  BaseGripperPlanner(gripper_goal_wrist, initial_gripper_tf, base_goal, initial_base_tf, success_thres_dist, success_thres_rot,
                     min_planner_velocity, max_planner_velocity, slow_down_factor, head_start, time_step_train,
                     is_analytic_env) {
  initial_dist_to_gripper_goal_ = (gripper_goal_wrist_.getOrigin() - initial_gripper_tf_.getOrigin()).length();

  prev_plan_.next_gripper_tf = initial_gripper_tf_;
  prev_plan_.next_base_tf = initial_base_tf_;
};

tf::Vector3 LinearPlanner::getVel(const tf::Transform &current, const tf::Transform &goal, double min_vel, double max_vel) {
  tf::Vector3 vec_to_goal = (goal.getOrigin() - current.getOrigin());
  return utils::normScaleVel(vec_to_goal / 100.0, min_vel, max_vel);
}

tf::Quaternion LinearPlanner::getRot(const tf::Transform &initial, const tf::Transform &next, const tf::Transform &goal,
                                     double initial_dist) {
  double dist_to_goal_post = (goal.getOrigin() - next.getOrigin()).length();
  double slerp_pct = utils::clampDouble(1.0 - dist_to_goal_post / initial_dist, 0.0, 0.9999);
  tf::Quaternion planned_q = initial.getRotation().slerp(goal.getRotation(), slerp_pct);
  planned_q.normalize();
  return planned_q;
}

GripperPlan LinearPlanner::calcNextStep(const GripperPlan &prev_plan, const double &dt, const double &min_velocity,
                                        const double &max_velocity) {
  GripperPlan plan;
  double min_vel = min_velocity * dt;
  double max_vel = max_velocity * dt;

  // new velocities based on distance to current Goal
  tf::Vector3 planned_gripper_vel = getVel(prev_plan.next_gripper_tf, gripper_goal_wrist_, min_vel, max_vel);
  tf::Vector3 planned_base_vel;
  planned_base_vel.setValue(planned_gripper_vel.x(), planned_gripper_vel.y(), 0.0);

  plan.next_gripper_tf.setOrigin(prev_plan.next_gripper_tf.getOrigin() + planned_gripper_vel);
  plan.next_base_tf.setOrigin(prev_plan.next_base_tf.getOrigin() + planned_base_vel);

  // new rotations: interpolated from start to gaol based on distance achieved so far
  tf::Quaternion planned_gripper_q =
    getRot(initial_gripper_tf_, plan.next_gripper_tf, gripper_goal_wrist_, initial_dist_to_gripper_goal_);
  plan.next_gripper_tf.setRotation(planned_gripper_q);
  // base
  // a) do not rotate
  plan.next_base_tf.setRotation(prev_plan.next_base_tf.getRotation());
  // b) rotate to match yaw of next gripper plan
  // tf::Vector3 next_gripper_rpy = utils::q_to_rpy(planned_gripper_q);
  // tf::Quaternion next_base_q;
  // next_base_q.setRPY(0.0, 0.0, next_gripper_rpy.z());
  // plan.nextBaseTransform.setRotation(next_base_q);

  // tf::Transform ggoal_floor;
  // ggoal_floor.setOrigin(tf::Vector3(gripper_goal_.getOrigin().x(), gripper_goal_.getOrigin().y(), 0.0));
  // tf::Vector3 ggoal_rpy = utils::q_to_rpy(gripper_goal_.getRotation());
  // tf::Quaternion ggoal_q;
  // ggoal_q.setRPY(0.0, 0.0, ggoal_rpy.z());
  // ggoal_floor.setRotation(ggoal_q);
  // tf::Quaternion next_base_q = get_rot(prevPlan.nextBaseTransform, prevPlan.nextBaseTransform, ggoal_floor,
  // (ggoal_floor.getOrigin() - initial_base_tf_.getOrigin()).length()); plan.nextBaseTransform.setRotation(next_base_q);
  return plan;
}

GripperPlan LinearPlanner::internalStep(double time, double dt, const RobotObs &robot_obs, const double &learned_vel_norm,
                                        bool update_prev_plan) {
  //     ROS_INFO("linearPlanner time: %f, dt: %f", time, dt);

  double min_vel, max_vel;
  if (learned_vel_norm >= 0.0) {
    min_vel = learned_vel_norm;
    max_vel = learned_vel_norm;
  } else {
    min_vel = min_planner_velocity_;
    max_vel = max_planner_velocity_;
  }

  GripperPlan next_plan = calcNextStep(prev_plan_, dt, min_vel, max_vel);
  if (update_prev_plan) {
    prev_plan_ = next_plan;
  }

  return next_plan;
}
