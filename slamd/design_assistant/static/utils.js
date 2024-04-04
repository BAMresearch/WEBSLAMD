export function assignClickEventToSubmitButton(button_id, handle_function) {
    const submit_button = document.getElementById(button_id);
    if (submit_button) {
        submit_button.addEventListener("click", handle_function);
    }
}

export function countSelectedOptions(options) {
    let count = 0;
    options.forEach(function (option) {
        if (option.checked) {
            ++count;
        }
    });
    return count;
}

export function scrollDown() {
    let chatWindow = document.getElementById('chat_window');
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

export function updateProgress() {
    let progressBar = document.getElementById('chat_progress');
    progressBar.value = progressBar.value + 1;
}