import ApiInstance from './API';

async function getShowings () {
  try {
    const { data } = await ApiInstance.get('/showings');

    return data ?? [];
  } catch (error) {
    console.error(error);
    return [];
  }
}

async function getShowing ({ showingId }) {
  try {
    const { data } = await ApiInstance.get(`/showing/${showingId}`);

    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
}

export {
  getShowing,
  getShowings,
};
