import ApiInstance from './API';

async function login ({ 
  email,
  password,
}) {
  try {
    const { data, status } =  await ApiInstance.post('/login', {
      email,
      password,
    });

    if (status === 200) { return data; }

    return null;
  } catch (error) {
    console.error(error);
    return null;
  }
};

async function register ({
  email,
  password,
  phone_number,
  name,
}) {
  try {
    const { data } =  await ApiInstance.post('/register', {
      email,
      password,
      phone_number,
      name,
    });

    return data;
  } catch (error) {
    console.error(error);
    return null;
  }
};

export {
  login,
  register,
};
