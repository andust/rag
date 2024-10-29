"use client";

import { useContext } from "react";
import { UserContext } from "@/app/_context/userContext";
import LogoutButton from "@/app/_molecules/logout-button/LogoutButton";

export default function Header() {
  const { user } = useContext(UserContext);
  
  return (
    <header className="flex justify-between container">
      User: {user?.email}
      <LogoutButton>Logout</LogoutButton>
    </header>
  );
}
