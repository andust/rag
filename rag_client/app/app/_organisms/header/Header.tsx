"use client";

import { useContext } from "react";
import { UserContext } from "@/app/_context/userContext";
import LogoutButton from "@/app/_molecules/logout-button/LogoutButton";
import Link from "next/link";

export default function Header() {
  const { user } = useContext(UserContext);
  
  return (
    <header className="flex justify-between items-center container">
      User: {user?.email}
      <Link href="/">Home</Link>
      <Link href="/chat/new">New chat</Link>
      <LogoutButton>Logout</LogoutButton>
    </header>
  );
}
