"use client";

import { UserContext } from "@/app/_context/userContext";
import { useContext } from "react";

export default function Header() {
  const { user } = useContext(UserContext);
  
  return (
    <header>
      User: {user?.email}
    </header>
  );
}
