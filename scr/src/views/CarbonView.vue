<template>
  <div class="carbon">
    <h2 class="carbon__title">My Carbon Savings</h2>

    <div class="carbon__hero-row">
      <CarbonSavingsHero />
      <CarbonStatsBar />
    </div>

    <div class="carbon__grid carbon__grid--3">
      <CO2Chart
        title="CO2 saved over time"
        type="line"
        :fetchData="getCO2SavedOverTime"
        :buildLabels="(d) => d.labels"
        :buildDatasets="
          (d) => [
            {
              label: 'Saved',
              data: d.data,
              borderColor: '#a3e635',
              backgroundColor: 'transparent',
              tension: 0.4,
              pointBackgroundColor: '#a3e635',
            },
          ]
        "
      />
      <TopUsersList title="Top Spenders" :fetchData="getTopSpenders" />
      <TopUsersList title="Top Savers" :fetchData="getTopSavers" />
    </div>

    <div class="carbon__grid carbon__grid--3">
      <CO2Chart
        title="CO2 emissions over time"
        type="line"
        :fetchData="getCO2EmissionsOverTime"
        :buildLabels="(d) => d.labels"
        :buildDatasets="
          (d) => [
            {
              label: 'Emissions',
              data: d.data,
              borderColor: '#5d9628',
              backgroundColor: 'rgba(93,150,40,0.1)',
              fill: true,
              tension: 0.4,
            },
          ]
        "
      />
      <CO2Chart
        title="CO2 Emissions by Model"
        type="pie"
        :fetchData="getCO2ByModel"
        :buildLabels="(d) => d.labels"
        :buildDatasets="
          (d) => [
            {
              data: d.data,
              backgroundColor: ['#343C6A', '#5d9628', '#a3e635', '#DEFE65'],
            },
          ]
        "
      />
      <CO2Chart
        title="CO2 Emissions by Team"
        type="doughnut"
        :fetchData="getCO2ByTeam"
        :buildLabels="(d) => d.labels"
        :buildDatasets="
          (d) => [
            {
              data: d.data,
              backgroundColor: ['#a3e635', '#06b6d4', '#343C6A', '#DEFE65'],
            },
          ]
        "
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import CarbonSavingsHero from '@/components/carbon/CarbonSavingsHero.vue'
import CarbonStatsBar from '@/components/carbon/CarbonStatsBar.vue'
import CO2Chart from '@/components/carbon/CO2Chart.vue'
import TopUsersList from '@/components/carbon/TopUsersList.vue'
import {
  getCO2SavedOverTime,
  getCO2EmissionsOverTime,
  getCO2ByModel,
  getCO2ByTeam,
  getTopSpenders,
  getTopSavers,
} from '@/services/dashboardService'
</script>

<style scoped src="@/assets/carbon/CarbonView.css" />