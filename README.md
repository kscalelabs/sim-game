# sim-game

TEST

This is a simplified implementation of controlling the Stompy arm in ManiSkill, for debugging issues with the model.

## Getting Started

1. Install [ManiSkill](https://maniskill.readthedocs.io/en/latest/user_guide/getting_started/installation.html)
2. Install this package:

```bash
git clone git@github.com:kscalelabs/sim-game.git
cd sim-game && pip install -e '.[dev]'
```

### Running the Simulation

To control the Stompy arm, use the command:

```bash
python -m simgame.scripts.control_robot
```

To show human rendering, use:

```bash
python -m simgame.scripts.control_robot --render-mode human
```

## Notes

### Random movements

When actions are disabled, there are still lots of eratic movements, suggesting that there are really large forces acting on the joints. To debug this, we should visualize the forces on the joints somehow.

### Installing ManiSkill

Ben tried installing ManiSkill to a cluster and found it very difficult. Somehow Allen installed it without any problems though. If you run into issues, you can ask Allen to work his magic.
