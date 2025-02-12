<template>
  <router-link
    class="movie-card"
    :to="`/showing/${movie.showing_id}`"
  >
    <img
      v-if="movieImage"
      :src="movieImage"
      width="80"
      height="120"
      alt=""
    >

    <div
      v-else
      class="movie-card__image-placeholder"
    >
      <v-icon size="x-large">
        mdi-image-off
      </v-icon>
    </div>

    <div class="movie-card__content">
      <h2>{{ movieName }}</h2>
      <span v-if="movieDate">{{ movieDate }}</span>

      <div class="mt-auto">
        Sala: {{ movie.hall_name }}
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue';

const MOVIE_IMAGES = {
  "Thor: The Dark World": "https://fwcdn.pl/fpo/25/64/622564/7570166_2.3.jpg",
  "Ratatouille": "https://resizing.flixster.com/ySiX7RlyKRuuxCcAI7SgdkMAZ0U=/ems.cHJkLWVtcy1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
  "Double Jeopardy": "https://m.media-amazon.com/images/M/MV5BZGFhMzVkYmQtYzI4OS00ZTYxLThjYTItYzZjYzY2OTlkMGQ4XkEyXkFqcGc@._V1_.jpg",
  "Big Daddy": "https://m.media-amazon.com/images/M/MV5BZGQwMzAyMjEtYjNiNi00NWQwLThiNjQtY2Q2ZWQ5ZGIzMDI4XkEyXkFqcGc@._V1_.jpg",
  "Divergent": "https://m.media-amazon.com/images/M/MV5BMTYxMzYwODE4OV5BMl5BanBnXkFtZTgwNDE5MzE2MDE@._V1_.jpg",
  "GoldenEye": "https://m.media-amazon.com/images/M/MV5BOGQxNmYyY2YtZGIyNy00ODgxLThhZWEtZGIyNjJhYzFlOTllXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
  "The Twilight Saga: New Moon": "https://m.media-amazon.com/images/M/MV5BMTI3MjE3NDIxNF5BMl5BanBnXkFtZTcwODM3NTY5Mg@@._V1_.jpg",
  "The Firm": "https://m.media-amazon.com/images/I/813fhhpmQhL.jpg",
  "Kindergarten Cop": "https://m.media-amazon.com/images/M/MV5BMjMyMTIyOTc0N15BMl5BanBnXkFtZTgwODY1NTk4NjE@._V1_.jpg",
  "The Mummy": "https://upload.wikimedia.org/wikipedia/en/6/68/The_mummy.jpg",
  "Live Free or Die Hard": "https://play-lh.googleusercontent.com/u2j2cU8PpV4ZYiOtezxIGXhGVb0p8Gu0AD4TYllcooH-17CVxCRPPY5NdNoeaKBbKdxPmw",
  "Misery": "https://m.media-amazon.com/images/M/MV5BNzY0ODQ3MTMxN15BMl5BanBnXkFtZTgwMDkwNTg4NjE@._V1_FMjpg_UX1000_.jpg",
  "Wild Wild West": "https://m.media-amazon.com/images/M/MV5BOGI1OWJjMWUtOTNiNC00N2RlLWE3OTYtM2FmOGUzNTQxNzk2XkEyXkFqcGc@._V1_.jpg",
  "Night at the Museum": "https://m.media-amazon.com/images/M/MV5BNGMyYjYyZDAtNzRiZC00ZjRkLTkwYjktODkxODQzNTFiMTVmXkEyXkFqcGc@._V1_.jpg",
  "The Rock": "https://upload.wikimedia.org/wikipedia/en/8/82/The_Rock_%28movie%29.jpg",
  "The General's Daughter": "https://m.media-amazon.com/images/M/MV5BNmZiZjk0OTQtZDhiNS00YzRjLWJmOWItZjM3ZGI4NDU5NDE0XkEyXkFqcGc@._V1_.jpg",
  "Beauty and the Beast": "https://lumiere-a.akamaihd.net/v1/images/p_beautyandthebeast1991_20488_592ec4b5.jpeg",
  "Wedding Crashers": "https://m.media-amazon.com/images/M/MV5BYzQwNmU0NGEtZjlmYy00ZjQ5LTlmMWYtODY3YzI4NTdiYzA4XkEyXkFqcGc@._V1_.jpg",
  "Phenomenon": "https://upload.wikimedia.org/wikipedia/en/b/bc/Phenomenonposter.jpg",
  "Presumed Innocent": "https://m.media-amazon.com/images/M/MV5BMjMyODU4NjQwMV5BMl5BanBnXkFtZTgwMTkwNTg4NjE@._V1_FMjpg_UX1000_.jpg",
  "Dinosaur": "https://resizing.flixster.com/-XZAfHZM39UwaGJIFWKAE8fS0ak=/v3/t/assets/p24980_p_v10_aa.jpg",
  "The Ring": "https://upload.wikimedia.org/wikipedia/en/3/37/Theringpostere.jpg",
  "Enchanted": "https://m.media-amazon.com/images/M/MV5BMjE4NDQ2Mjc0OF5BMl5BanBnXkFtZTcwNzQ2NDE1MQ@@._V1_FMjpg_UX1000_.jpg",
  "Shakespeare in Love": "https://m.media-amazon.com/images/M/MV5BYmM3MTllNzYtN2MzNS00NWQwLTk0NTEtNjY1MmMwYjNkNTE5XkEyXkFqcGc@._V1_.jpg",
  "Star Wars: Episode I - The Phantom Menace": "https://m.media-amazon.com/images/M/MV5BODVhNGIxOGItYWNlMi00YTA0LWI3NTctZmQxZGUwZDEyZWI4XkEyXkFqcGc@._V1_.jpg"
};

const props = defineProps({
  movie: {
    type: Object,
    required: true,
  }
});

const movieName = computed(() => {
  return props.movie?.movie_title ?? props.movie?.movie ?? null;
})

const movieDate = computed(() => {
  const showingDate = props.movie?.showing_date;
  if (!showingDate) { return null; }

  const parsedDate = new Date(showingDate);
  return new Intl.DateTimeFormat('pl', { dateStyle: 'medium', timeStyle: 'short' }).format(parsedDate);
})

const movieImage = computed(() => {
  return MOVIE_IMAGES[movieName.value];
});
</script>

<style lang="scss">
.movie-card {
  --shadow-1: rgba(0, 0, 0, 0.2);
  --shadow-2: rgba(0, 0, 0, 0.14);
  --shadow-3: rgba(0, 0, 0, 0.12);

  border-radius: 20px;
  padding: 14px;
  min-height: 60px;
  cursor: pointer;
  display: flex;
  flex-direction: row;
  gap: 12px;
  text-decoration: none;
  color: #000;
  background-color: #fff;
  transition: all ease-in-out 0.3s;
  box-shadow: 0px 2px 1px -1px var(--shadow-1),
    0px 1px 1px 0px var(--shadow-2),
    0px 1px 3px 0px var(--shadow-3);

  & > img {
    border-radius: 10px;
  }

  &:hover {
    --shadow-1: rgba(0, 150, 136, 0.2);
    --shadow-2: rgba(0, 150, 136, 0.14);
    --shadow-3: rgba(0, 150, 136, 0.12);
    background-color: #f2f2f2;

    & > .movie-card__image-placeholder {
      background-color: #fff;
    }
  }

  &__content {
    color: #000;
    display: flex;
    flex-direction: column;

    & > h2 {
      font-size: 20px;
    }

    & > span {
      color: rgba(0, 0, 0, .6);
      font-size: 14px;
    }
  }

  &__image-placeholder {
    border-radius: 10px;
    width: 80px;
    min-width: 80px;
    height: 120px;
    background-color: #f2f2f2;
    transition: all ease-in-out 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
}
</style>