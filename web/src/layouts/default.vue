<template>
  <v-main>
    <v-app-bar
      scroll-behavior="elevate"
      color="teal"
    >
      <v-app-bar-title>
        <router-link
          to="/"
          class="header-link"
        >
          CinemaTickets
        </router-link>
      </v-app-bar-title>

      <div
        v-if="userIsLoggedIn"
        class="d-flex px-5"
      >
        <v-icon class="mr-2">
          mdi-account
        </v-icon>
        Witaj {{ userName }}
      </div>
    </v-app-bar>
    <router-view />
  </v-main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const userName = ref('');

const userIsLoggedIn = ref(false);

onMounted(() => {
  const userData = localStorage.getItem('userData');

  if (userData) {
    userIsLoggedIn.value = true;

    const parsedData = JSON.parse(userData);
    userName.value = parsedData.name;
  } else {
    router.push('/auth');
  }
});
</script>


<style lang="scss">
.header-link {
  text-decoration: none;
  color: #fff;
  cursor: pointer;
  font-weight: normal;
}
</style>
