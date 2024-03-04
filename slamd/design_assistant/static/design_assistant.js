import { assignClickEventToSubmitButton } from "./utils.js";
import { assignClickEventToTaskForm} from "./task.js"
import { assignClickEventToImportForm } from "./import.js"
import { assignClickEventToMaterialTypeField } from "./material_type.js";
import { assignClickEventToDesignTargetForm, handleDesignTargetsSubmission, handleAddingDesignTargets } from "./target.js";
import { assignClickEventToPowdersForm, handlePowdersSubmission } from "./powder.js";
import { assignClickEventToLiquidForm, handleLiquidSubmission, handleAddingLiquid } from "./liquid.js";
import { assignClickEventToOtherForm, handleOtherSubmission, handleAddingOther } from "./other.js";
import { assignInputEventToCommentForm, handleCommentSubmission} from "./comment.js";
import { handleDeleteDesignAssistantSession } from "./session.js"

window.addEventListener("load", function () {
  assignClickEventToSubmitButton(
    "delete_session_button",
    handleDeleteDesignAssistantSession
  );
  assignClickEventToTaskForm();
  assignClickEventToImportForm();
  assignClickEventToMaterialTypeField();
  assignClickEventToSubmitButton(
    "design_targets_submit_button",
    handleDesignTargetsSubmission
  );
  assignClickEventToSubmitButton(
    "powders_submit_button",
    handlePowdersSubmission
  );
  assignClickEventToDesignTargetForm();
  assignClickEventToPowdersForm();
  assignClickEventToSubmitButton(
    "additional_design_targets_button",
    handleAddingDesignTargets
  );
  assignClickEventToSubmitButton(
    "submit_liquid_button",
    handleLiquidSubmission
  );
  assignClickEventToSubmitButton(
    "additional_liquid_button",
    handleAddingLiquid
  );
  assignClickEventToLiquidForm();
  assignClickEventToSubmitButton("submit_other_button", handleOtherSubmission);
  assignClickEventToSubmitButton("additional_other_button", handleAddingOther);
  assignClickEventToOtherForm();
  assignInputEventToCommentForm();
  assignClickEventToSubmitButton(
    "submit_comment_button",
    handleCommentSubmission
  );
});
