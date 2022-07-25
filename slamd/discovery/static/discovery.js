function updateCuriosityValue(curiosity) {
    // Round the value to two decimal places
    document.getElementById('selected-range').value = Math.round(curiosity * 100) / 100;
}