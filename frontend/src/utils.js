export const displayRunDuration = (durationMins) => {
    let hours = Math.floor(durationMins / 60)
    let withoutHours = durationMins - hours * 60
    let minutes = Math.floor(withoutHours)
    let withoutMinutes = withoutHours - minutes
    let seconds = Math.floor(60 * withoutMinutes)
    if (hours > 0) {
        return hours + ' hours, ' + minutes + ' mins'
    }
    return minutes + ' mins, ' + seconds + ' secs'
}