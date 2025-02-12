<template>
  <v-container>
    <v-responsive
      class="align-center fill-height mx-auto"
      max-width="800"
    >
      <common-loader v-if="loading" />

      <template v-else-if="!loading && showSuccess">
        <div class="showing-container__message-screen">
          <v-icon
            color="success"
            :size="64"
          >
            mdi-check-circle-outline
          </v-icon>

          <div>
            <span>
              Rezerwacja udana!
            </span>

            <p>Sposób płatności: Płatność na miejscu</p>

            <p>Wszystkie informację znajdziesz na mailu: <b>{{ userEmail }}</b></p>
          </div>
        </div>
      </template>

      <div
        v-else
        class="showing-container"
      >
        <div class="showing-container__page-header">
          <the-movie-card
            v-if="movieData"
            :movie="movieData"
          />

          <div class="showing-container__page-info">
            <span>Wybrane miejsca ({{ selectedSeats.length }})</span>
            <ul>
              <li
                v-for="item in selectedSeatsText"
                :key="item"
              >
                {{ item }}
              </li>
            </ul>
          </div>
        </div>

        <template v-if="hasAvailableSeats">
          <div class="showing-container__screen" />

          <div
            class="showing-container__seat-map"
          >
            <div
              v-for="row in Object.keys(availableSeats)"
              :key="row"
              class="showing-container__seat-map-row"
            >
              <div class="showing-container__seat-map-row-number">
                {{ row }}.
              </div>

              <div
                v-for="seat in availableSeats[row]"
                :key="seat.seat_id"
                class="showing-container__seat-map-seat"
                :class="{
                  'showing-container__seat-map-seat--is-selected': isSeatSelected(seat.seat_id),
                  'showing-container__seat-map-seat--is-reserved': seat.is_reserved,
                }"
                @click="selectSeat(seat)"
              >
                {{ seat.seat_number }}
              </div>

              <div class="showing-container__seat-map-row-number">
                {{ row }}.
              </div>
            </div>
          </div>

          <div class="mt-6">
            <v-btn
              block
              :disabled="!selectedSeats.length"
              @click="submitReservation"
            >
              Zarezerwuj miejsca ({{ selectedSeats.length }})
            </v-btn>
          </div>
        </template>

        <div
          v-else
          class="showing-container__message-screen mt-15"
          style="height: unset;"
        >
          <v-icon
            color="error"
            :size="64"
          >
            mdi-close-circle-outline
          </v-icon>

          <div>
            <span>Wszystkie miejsca wyprzedane :(</span>
            <p>Wygląda na to, że to bardzo popularny film</p>
          </div>
        </div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script setup>
import { setReservation } from '@/services/reserveService';
import { getShowing } from '@/services/showingService';
import { computed, onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const loading = ref(false);

const showSuccess = ref(false);

const availableSeats = ref({});

const selectedSeats = ref([]);

const movieData = ref({});

const userEmail = ref(null);

const hasAvailableSeats = ref(false);

const selectedSeatsText = computed(() => {
  return selectedSeats.value.reduce((acc, seat) => {
    acc.push(`Rząd ${seat.row_number}, Miejsce ${seat.seat_number}`);
    return acc;
  }, []);
});

onMounted(async () => {
  loading.value = true;
  
  const result = await getShowing({ showingId: route?.params?.showingId });

  const seats = result?.available_seats ?? [];

  hasAvailableSeats.value = seats.some(({ is_reserved }) => !is_reserved);

  availableSeats.value = Object.groupBy(seats, ({ row_number }) => row_number);

  movieData.value = {
    ...result,
    available_seats: undefined,
  };

  loading.value = false;
});

function isSeatSelected(seatId) {
  return selectedSeats.value.findIndex(({ seat_id }) => seat_id === seatId) !== -1;
}

function selectSeat (seatData) {
  const seatIsSelected = isSeatSelected(seatData.seat_id);

  if (seatIsSelected) {
    selectedSeats.value = selectedSeats.value.filter(({ seat_id }) => seat_id !== seatData.seat_id);
  } else {
    selectedSeats.value.push(seatData);
  }
}

async function submitReservation () {
  loading.value = true;

  const userData = JSON.parse(localStorage.getItem('userData'));

  const response = await setReservation({
    seat_ids: selectedSeats.value.map(({ seat_id }) => seat_id),
    showing_id: movieData.value.showing_id,
    user_id: userData.user_id,
  });

  showSuccess.value = response;
  userEmail.value = userData.email;

  loading.value = false;
}
</script>

<style lang="scss">
.showing-container {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 20px;

  &__page-header {
    display: flex;
    flex-direction: row;
    flex-wrap: nowrap;
    gap: 16px;

    & > a {
      pointer-events: none;
      width: fit-content;
      min-width: 400px;
      height: fit-content;
    }
  }

  &__page-info {
    display: flex;
    flex-direction: column;

    & > span {
      font-weight: 600;
      font-size: 18px;
    }

    & > ul {
      list-style-type: none;
      margin: 0;
      padding: 0;
    }
  }

  &__screen {
    margin-top: 40px;
    margin-bottom: 40px;
    width: 100%;
    height: 10px;
    background-color: gray;
    border-top-left-radius: 20px;
    border-top-right-radius: 20px;
    position: relative;

    &::after {
      content: 'Ekran';
      position: absolute;
      text-transform: uppercase;
      color: rgba(0, 0, 0, .4);
      font-weight: 500;
      font-size: 14px;
      top: 12px;
      left: 50%;
    }
  }

  &__seat-map {
    display: flex;
    flex-direction: column;
    gap: 8px;

    &-row {
      display: flex;
      flex-direction: row;
      flex-wrap: nowrap;
      align-items: center;
      gap: 4px;

      &-number {
        font-size: 20px;
        font-weight: 700;
        color: rgba(0, 0, 0, 0.5);

        &:first-of-type {
          margin-right: auto;
        }

        &:last-of-type {
          margin-left: auto;
        }
      }
    }

    &-seat {
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 4px;
      width: 40px;
      aspect-ratio: 1/1;
      height: 40px;
      background-color: #f2f2f2;
      cursor: pointer;
      transition: all ease-in-out 0.3s;

      &:hover {
        background-color: rgba(0, 150, 136, 0.3);
      }

      &--is-selected {
        background-color: rgb(0, 150, 136);
        color: #fff;

        &:hover {
          background-color: rgba(0, 150, 136, 0.8);
        }
      }

      &--is-reserved {
        cursor: not-allowed;
        pointer-events: none;
        background-color: #000;
        opacity: .3;
        color: #000;
      }
    }
  }

  &__message-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 24px;
    height: 70vh;
    justify-content: center;

    & > div {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 4px;

      & > span {
        font-size: 24px;
        font-weight: 500;
      }

      & > p {
        font-weight: 14px;
      }
    }
  }
}
</style>