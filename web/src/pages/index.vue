<template>
  <v-container>
    <v-responsive
      class="align-center fill-height mx-auto"
      max-width="800"
    >
      <h1 class="px-5">
        Repertuar kina na {{ currentDate }}
      </h1>

      <common-loader v-if="loading" />

      <div
        v-else
        class="movies__container"
      >
        <the-movie-card
          v-for="movie in movies"
          :key="movie.showing_id"
          :movie="movie"
        />
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { getShowings } from '@/services/showingService';
import { computed, onMounted, ref } from 'vue';

const movies = ref([]);

const loading = ref(false);

const currentDate = computed(() => {
  return new Intl.DateTimeFormat('pl', { dateStyle: 'medium' }).format(new Date());
})

onMounted(async () => {
  loading.value = true;
  const result = await getShowings();

  movies.value = result
    .sort((a, b) => new Date(a.showing_date) - new Date(b.showing_date));
  loading.value = false;
});
</script>

<style lang="scss">
.movies__container {
  display: grid;
  padding: 20px;
  gap: 8px;
  grid-template-columns: repeat(2, 1fr);
}
</style>