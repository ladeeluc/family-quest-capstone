function getDateString(date) {
    return (
        date.toLocaleDateString([], { year:'numeric', month:'short', day:'numeric' }) +
        " at " +
        date.toLocaleTimeString([], {timeStyle: 'short'})
    )
}