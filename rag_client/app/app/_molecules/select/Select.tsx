"use client";

import { ReactNode, useEffect, useRef, useState } from "react";

import "./select.css";

export interface Option {
  label: string | ReactNode;
  value: string | number;
}

interface SelectProps {
  options: Option[];
  label: string;
  onOptionChange: (option: Option) => void;
  defaultOption?: Option | null;
}

const Select = ({ options, label, onOptionChange, defaultOption = null }: SelectProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedOption, setSelectedOption] = useState<Option | null>(defaultOption);
  const selectRef = useRef<HTMLDivElement>(null);

  const showClassName = isOpen ? " show" : "";

  const toggleSelect = () => {
    setIsOpen(!isOpen);
  };

  const handleOptionClick = (option: Option) => {
    setSelectedOption(option);
    onOptionChange(option);
    setIsOpen(false);
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      selectRef.current &&
      !selectRef.current.contains(event.target as Node)
    ) {
      setIsOpen(false);
    }
  };

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, []);

  return (
    <div className="relative" ref={selectRef}>
      <button
        onClick={toggleSelect}
        className="w-full relative z-20 bg-black p-2 border rounded text-left"
      >
        {selectedOption?.label || label}
      </button>
      <ul
        className={`absolute z-10 w-full mt-1 bg-black border rounded transition-all duration-200 ease-in-out${showClassName}`}
      >
        {options.map((option) => (
          <li
            key={option.value}
            onClick={() => handleOptionClick(option)}
            className="p-2 hover:bg-gray-700 cursor-pointer"
          >
            {option.label}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Select;
