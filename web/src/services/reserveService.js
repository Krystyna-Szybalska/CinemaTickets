import ApiInstance from './API';

async function setReservation ({
  showing_id,
  user_id,
  seat_ids,
}) {
  try {
    const { data } = await ApiInstance.post('/reserve', {
      showing_id,
      user_id,
      seat_ids,
    })

    return data?.message === "Reservation successful";
  } catch (error) {
    console.error(error);
    return false;
  }
};

export {
  setReservation,
};
