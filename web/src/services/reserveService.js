import ApiInstance from './API';

async function setReservation ({
  showing_id,
  user_id,
  seat_ids,
}) {
  try {
    const result = await ApiInstance.post('/reserve', {
      showing_id,
      user_id,
      seat_ids,
    })

    return result?.message === "Reservation successful";
  } catch (error) {
    console.error(error);
    return false;
  }
};

export {
  setReservation,
};
