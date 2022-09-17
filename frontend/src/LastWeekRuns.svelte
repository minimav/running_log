<script>
    import { onMount } from "svelte";
    import { fade } from "svelte/transition";
    import Emoji from "svelte-emoji";
    import LastWeekRunsSummary from "./LastWeekRunsSummary.svelte";
    import { displayRunDuration } from "./utils.js";
    import { distanceUnitStore } from "./stores.js";

    let lastWeekRunsByDay = [],
        lastWeekRuns = [],
        distanceUnit;

    distanceUnitStore.subscribe((value) => {
        distanceUnit = value;
    });

    $: lastWeekRuns = lastWeekRunsByDay.filter(
        (run) => run.distance_miles && run.duration_mins
    );

    onMount(async () => {
        distanceUnitStore.useLocalStorage();
        const results = await fetch(
            "http://localhost:8080/recent_runs?num_days=7"
        );
        lastWeekRunsByDay = await results.json();
    });

    const deleteRun = (date) => {
        fetch("http://localhost:8080/delete_run?date=" + date, {
            method: "GET",
            headers: { "Content-Type": "application/json" },
        }).then(function (response) {
            if (response.status == 404) {
                response.json().then((body) => {
                    alert(body.detail);
                });
            } else {
                location.reload();
            }
        });
    };

    const speedOfRun = (run, distanceUnit) => {
        let minsPerMile = run.duration_mins / run.distance_miles;
        return distanceUnit === "miles" ? minsPerMile : minsPerMile / 1.609;
    };

    const getSpeedEmoji = (minsPerMile) => {
        if (minsPerMile < 7.25) {
            return "🔥";
        } else if (minsPerMile < 7.8) {
            return "🏃‍♂️";
        } else {
            return "🐌";
        }
    };

    const getRunDistance = (run, distanceUnit) => {
        return distanceUnit === "miles"
            ? run.distance_miles
            : run.distance_miles * 1.609;
    };
</script>

{#if lastWeekRuns.length > 0}
    <div class="last-week-runs">
        {#each lastWeekRunsByDay as run}
            {#if run.distance_miles && run.duration_mins}
                <div
                    transition:fade={{ duration: 2000 }}
                    class="last-week-run last-week-run-exists"
                >
                    <p class="last-week-run-date">{run.date}</p>
                    <p class="last-week-run-distance">
                        {getRunDistance(run, distanceUnit).toFixed(2)}
                        {distanceUnit}
                    </p>
                    <p class="last-week-run-duration">
                        {displayRunDuration(run.duration_mins)}
                    </p>
                    <p class="last-week-run-speed">
                        {speedOfRun(run, distanceUnit).toFixed(2)} mins/{distanceUnit}
                        <Emoji
                            symbol={getSpeedEmoji(
                                run.duration_mins / run.distance_miles
                            )}
                        />
                    </p>
                    <button
                        class="delete-run-btn"
                        on:click={deleteRun(run.date)}
                    >
                        Delete
                    </button>
                </div>
            {:else}
                <div
                    transition:fade={{ duration: 2000 }}
                    class="last-week-run last-week-run-empty"
                >
                    <p class="last-week-run-date">{run.date}</p>
                </div>
            {/if}
        {/each}
    </div>
    <LastWeekRunsSummary runs={lastWeekRuns} />
{:else}
    <div class="no-last-week-runs">No runs in the last week!</div>
{/if}

<style>
    .last-week-runs {
        width: 100%;
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        grid-gap: 8px;
    }

    .last-week-run {
        text-align: center;
        border-width: 2px;
        border-color: #ff3e00;
        border-radius: 25px;
    }

    .last-week-run-exists {
        border-style: solid;
    }

    .last-week-run-empty {
        border-style: dashed;
    }

    .last-week-run-date {
        font-size: 1.1em;
        font-weight: 500;
    }

    /* Responsive layout - when the screen is less than 600px wide, make a single column of last week's runs instead of a row */
    @media screen and (max-width: 600px) {
        .last-week-runs {
            grid-template-columns: repeat(1, 7fr);
        }
    }

    .delete-run-btn {
        background-color: #ff3e00;
        color: white;
        padding: 6px 10px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }

    .delete-run-btn:hover {
        background-color: #fa8761;
    }
</style>
