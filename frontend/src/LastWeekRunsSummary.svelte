<script>
    import { onMount } from 'svelte';
    import { fade } from 'svelte/transition';
    import { distanceUnitStore } from './stores.js';
    import { displayRunDuration } from './utils.js';
	export let runs;

    let distanceUnit, totalDistance = 0.0;

    distanceUnitStore.subscribe(value => {
		distanceUnit = value;
	});

    function calculateTotalDistance(runs, distanceUnit) {
        let distanceMiles = 0.0;
        runs.forEach(r => distanceMiles += r.distance_miles)
        return distanceUnit === "miles" ? distanceMiles : distanceMiles * 1.609
    }

    function calculateTotalDurationMins() {
        let durationMins = 0.0;
        runs.forEach(r => durationMins += r.duration_mins)
        return durationMins
    }

    $: totalDistance = calculateTotalDistance(runs, distanceUnit); 

    onMount(async () => {
        distanceUnitStore.useLocalStorage();
    })
</script>

<div transition:fade="{{ duration: 2000 }}" class="last-week-run-summary">
    <p>Total distance ({distanceUnit}): {totalDistance.toFixed(2)}, Total duration: {displayRunDuration(calculateTotalDurationMins())}</p>
</div>

<style>
    .last-week-run-summary {
        margin: auto;
        width: 50%;
        text-align: center;
        color: #FFF;
        background-color: #ff3e00;
        border-radius: 25px;
        border-style: solid;
        margin-top: 10px;
    }
</style>
