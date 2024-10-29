import { FormEvent } from "react";

interface Props {
  value: string | number;
  name?: string;
  type?: "text" | "password" | "file";
  placeholder?: string;
  onChange?: (e: FormEvent<HTMLInputElement>) => void;
}

export default function Input({
  value,
  name,
  type = "text",
  placeholder = "",
  onChange
}: Props) {
  return (
    <input
      className="border px-4 py-2 w-full"
      type={type}
      placeholder={placeholder}
      name={name}
      value={value}
      onChange={onChange}
    />
  );
}
