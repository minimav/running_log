<script>
    import { distanceUnitStore } from './stores';

    let distanceUnit;

	function setDistanceUnit(event) {
        distanceUnit = event.target.value
		distanceUnitStore.set(distanceUnit);
	}

    distanceUnitStore.subscribe(value => {
		distanceUnit = value;
	});
</script>

<label>
    <input checked={distanceUnit === 'km'} type=radio on:click={setDistanceUnit} value='km'>
    km
</label>
<label>
    <input checked={distanceUnit === 'miles'} type=radio on:click={setDistanceUnit} value='miles'>
    miles
</label>

<style>
    input, label { display: inline; }
</style>