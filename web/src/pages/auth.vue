<template>
  <v-container>
    <v-responsive
      class="align-center fill-height mx-auto"
      max-width="450"
    >
      <v-tabs
        v-model="tab"
        align-tabs="center"
      >
        <v-tab :value="1">
          Logowanie
        </v-tab>
        <v-tab :value="2">
          Rejestracja
        </v-tab>
      </v-tabs>

      <v-tabs-window v-model="tab">
        <v-tabs-window-item :value="1">
          <v-form
            ref="loginForm"
            @submit="onLoginSubmit"
          >
            <v-text-field
              v-model="loginFormData.email"
              label="Email"
              type="email"
              :rules="[required]"
            />

            <v-text-field
              v-model="loginFormData.password"
              label="Password"
              type="password"
              :rules="[required]"
            />

            <v-btn @click="onLoginSubmit">
              Zaloguj się
            </v-btn>
          </v-form>
        </v-tabs-window-item>

        <v-tabs-window-item :value="2">
          <v-form
            ref="registerForm"
            @submit="onRegisterSubmit"
          >
            <v-text-field
              v-model="registerFormData.name"
              label="Nazwa"
              type="text"
              :rules="[required]"
            />

            <v-text-field
              v-model="registerFormData.email"
              label="Email"
              type="email"
              :rules="[required]"
            />

            <v-text-field
              v-model="registerFormData.password"
              label="Hasło"
              type="password"
              :rules="[required]"
            />

            <v-text-field
              v-model="registerFormData.phoneNumber"
              label="Numer telefonu"
              type="tel"
              :rules="[required]"
            />

            <v-btn @click="onRegisterSubmit">
              Zarejestruj się
            </v-btn>
          </v-form>
        </v-tabs-window-item>
      </v-tabs-window>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue';
import { useValidation } from '@/composables/validation';
import { useRouter } from 'vue-router'

import { login, register } from '@/services/authService'

const router = useRouter()

const { required } = useValidation();

const loginForm = ref();

const registerForm = ref();

const tab = ref(1);

const loginFormData = reactive({
  email: '',
  password: '',
});

const registerFormData = reactive({
  email: '',
  password: '',
  name: '',
  phoneNumber: '',
});

onMounted(() => {
  const userIsLoggedIn = localStorage.getItem('userData');

  if (userIsLoggedIn) {
    router.push('/');
  }
})

async function onLoginSubmit () {
  if (!loginForm.value) { return; }

  const { valid } = await loginForm.value.validate();

  if (valid) {
    const result = await login({
      email: loginFormData.email,
      password: loginFormData.password,
    });

    saveUserData(result);
  }
}

async function onRegisterSubmit () {
  if (!registerForm.value) { return; }

  const { valid } = await registerForm.value.validate();

  if (valid) {
    const result = await register({
      email: registerFormData.email,
      password: registerFormData.password,
      name: registerFormData.name,
      phone_number: registerFormData.phoneNumber,
    });

    saveUserData(result);
  }
}

function saveUserData (data) {
  if (data) {
    localStorage.setItem('userData', JSON.stringify(data));
    router.push('/')
  }
}
</script>

<style lang="scss">
.v-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-block: 20px;
}
</style>
