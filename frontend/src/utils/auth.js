// frontend/src/utils/auth.js

export const getTokenInfo = () => {
  const token = localStorage.getItem("access_token");
  const user = localStorage.getItem("user");

  if (!token || !user) return null;

  try {
    return {
      token,
      ...JSON.parse(user),
    };
  } catch (err) {
    console.error("Invalid user data in localStorage", err);
    return null;
  }
};
