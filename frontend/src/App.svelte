
<script>
	import LogRun from './LogRun.svelte';
	import LastWeekRuns from './LastWeekRuns.svelte';
    import MileageChart from './MileageChart.svelte';
    import DistanceUnit from './DistanceUnit.svelte';
</script>

<main>
	<h1>Running log</h1>

	<h2>Distance unit</h2>
	<DistanceUnit/>

	<h2>Last week's runs</h2>
	<LastWeekRuns/>

	<h2 >Log a new run</h2>
	<LogRun/>

	<h2>Mileage</h2>
	<MileageChart/>
</main>

<style>
	main {
		padding: 1em;
		max-width: 1000px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	h2 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 1em;
		font-weight: 200;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>