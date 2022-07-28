function updateCuriosityValue(curiosity) {
    value = parseFloat(curiosity);
    document.getElementById('selected-range').value = parseFloat(value.toFixed(2));
}