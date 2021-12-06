#!/bin/sh

cp -r ./webots $WEBOTS_HOME/projects
cd $WEBOTS_HOME/projects/smpl_webots/libraries/smpl_util
make
cd $WEBOTS_HOME/projects/smpl_webots/controllers/smpl_animation
make
mkdir $WEBOTS_HOME/projects/smpl_webots/skins/model-204
cp $OPENDR_HOME/projects/simulation/SMPL+D_body_models/fbx_models/female/model-204/model-204.fbx $WEBOTS_HOME/projects/smpl_webots/skins/model-204/model-204.fbx
mkdir $WEBOTS_HOME/projects/smpl_webots/protos/textures/model-204
cp $OPENDR_HOME/projects/simulation/SMPL+D_body_models/fbx_models/female/model-204/texture.png $WEBOTS_HOME/projects/smpl_webots/protos/textures/model-204/texture.png
