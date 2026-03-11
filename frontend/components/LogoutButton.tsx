"use client";

export default function LogoutButton() {
  const handleLogout = () => {
    localStorage.removeItem("token");
    window.location.href = "/login";
  };

  return (
    <button className="soc-logout" onClick={handleLogout}>
      Logout
    </button>
  );
}
