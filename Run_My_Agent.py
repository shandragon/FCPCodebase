from agent.Base_Agent import Base_Agent as Agent
from scripts.commons.Script import Script
from math_ops.Math_Ops import Math_Ops as M

script = Script()
a = script.args

# define robot type
robot_type = (0,1,1,1,2,3,3,3,4,4,4)[a.u-1]

# define initial formation
init_pos = ([-14,0],[-9,-5],[-9,0],[-9,5],[-5,-5],[-5,0],[-5,5],[-1,-6],[-1,-2.5],[-1,2.5],[-1,6])[a.u-1] 

# Args: Server IP, Agent Port, Monitor Port, Uniform No., Robot Type, Team Name
player = Agent(a.i, a.p, a.m, a.u, robot_type, a.t)


w = player.world

getting_up = False

while True:
    player_2d = w.robot.loc_head_position[:2]
    ball_2d = w.ball_abs_pos[:2]
    goal_dir = M.vector_angle( (15,0)-player_2d ) # Goal direction

    if w.play_mode_group == w.MG_ACTIVE_BEAM:
        player.scom.commit_beam(init_pos, 0)

    if not w.robot.unum == 1:
        if player.behavior.is_ready("Get_Up")or getting_up:
            getting_up = not player.behavior.execute("Get_Up") # True on completion
        else:
            if ball_2d[0] > 0: # kick if ball is on opponent's side (x>0)
                player.behavior.execute("Basic_Kick", goal_dir)
            elif M.distance_point_to_segment(player_2d,ball_2d, ball_2d
                + M.normalize_vec( ball_2d-(15,0) ) ) > 0.1: # not aligned
                next_pos, next_ori, dist = player.path_manager.get_path_to_ball(
                x_ori=goal_dir, x_dev=-0.3, torso_ori=goal_dir)
                player.behavior.execute("Walk", next_pos, True, next_ori, True, dist)
            else:
                player.behavior.execute("Walk", w.ball_abs_pos[:2], True, goal_dir, True, 0.5)
    else:
        pass

    player.scom.commit_and_send( w.robot.get_command() )
    player.scom.receive()

    w.draw.annotation((*player_2d,0.6), "Hello!", w.draw.Color.white, "my_info",
flush=False)
    w.draw.line(player_2d, ball_2d, 3, w.draw.Color.yellow, "my_info", flush=True)

