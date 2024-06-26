# Description printed for the user in the UI
description = {
    "Torso Lean": """Slight forward lean while running lowers the stress on your knees. Too upright posture or leaning back might cause \"runner's knee\" syndrome, or in other words, pain in front of your knee and around your kneecap. In contrast, running bent too forwards moves the stress onto your hips and ankles. Ideal trunk lean should be around 7°, but 2°-10° is acceptable.""",
    "Knee Flexion": """During the phase where you're standing on one leg, your knee should flex to a maximum angle of at least 45°. This is where your body absorbs the impact from bodyweight moving onto a single leg. Values less than 40° can mean stiff knees which cause excessive stress on other joints and knees themselves.""",
    "Tibia Angle": """At the moment when a foot is hitting the ground and your weight is moved onto that leg, the angle of your tibia, or shin bone, makes a big difference. Imagine this as a position of your ankle versus the position of your knee. When the ankle is more forward, your knee can't flex freely and is hurting in the process. When your bodyweight moves onto the stance leg, the knee should be slightly forward or vertical with your ankle.""",
    "Center of Mass Displacement": "This metric determines the efficiency of your running form. If your body moves up and down too much, it means you're wasting energy. The body's center of mass should stay fairly level. It's calculated as an angle between the lowest point position of hips during the standing phase and their highest position while in the air. The maximal value is set to 10°.",
    "Elbow Angle": """Elbows should be at a 90° angle to gain optimal efficiency. However, it's okay to lower your arms one in a while to release some tension from your back and shoulders. Incorrect elbow position doesn't cause injuries, just a decrease in speed and power saving.""",
    "Hip Extension": """Hip extension is measured just after standing on a leg, when you start pushing off of the ground. It can be a sign of limited mobility. This occurrence is observed as an angle between the thigh and the vertical axis of the side view. Exact numbers can differ according to the runner's build but an angle lower than 10° can indicate limited flexion and possible future problems.""",
    "Feet Strike": "Focus on hitting the ground with the ball of your foot. Landing on the heel might indicate that you're taking too big steps and your joints are being damaged in the process. Striking with the front of your foot is okay in some cases, particularly when running hills. Angles of the foot with the ground bigger than 20° are considered risky.",
    "Pelvic Drop": """Your hip bones should stay fairly horizontal with each other while running. If one side drops significantly lower than the other, it could mean that your muscles in that area are weak or fatigued. The maximal expected angle between the bones is set to 6°. Although, impacts on injuries and efficiency were not yet studied.""",
}

# Keypoints used to calculate metric -> used to highlight in the UI
corresponding_keypoints = {
    "Torso Lean": ["Neck", "MidHip"],
    "Knee FlexionR": ["RAnkle", "RKnee", "RHip"],
    "Knee FlexionL": ["LAnkle", "LKnee", "LHip"],
    "Tibia AngleR": ["RAnkle", "RKnee"],
    "Tibia AngleL": ["LAnkle", "LKnee"],
    "Center of Mass Displacement": ["MidHip", "MidHip"],
    "Elbow AngleR": ["RWrist", "RElbow", "RShoulder"],
    "Elbow AngleL": ["LWrist", "LElbow", "LShoulder"],
    "Hip ExtensionR": ["LKnee", "LHip"],
    "Hip ExtensionL": ["RKnee", "RHip"],
    "Feet StrikeR": ["RHeel", "RBigToe"],
    "Feet StrikeL": ["LHeel", "LBigToe"],
    "Pelvic Drop": ["RHip", "LHip"],
}
