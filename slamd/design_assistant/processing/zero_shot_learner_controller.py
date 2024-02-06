from flask import Blueprint, render_template


zero_shot_learner = Blueprint(
    "zero_shot_prompting",
    __name__,
    template_folder="../templates",
    static_folder="../static",
    static_url_path="static",
    url_prefix="/design_assistant/zero_shot_learner",
)


@zero_shot_learner.route("", methods=["GET"])
def zero_shot_prompting_page():
    return render_template("zero_shot_learner.html")
