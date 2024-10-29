"use client";

import { UserProvider } from "./_context/userContext";
import { ChildrenProp } from "./types";

export default function Providers({ children }: ChildrenProp) {
  return (
    <UserProvider>
      {children}
    </UserProvider>
  );
}
