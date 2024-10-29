import { ChildrenProp, ClassNameProp } from "../../types";

export interface ThemeProp {
  theme?: "base" | "primary";
}

interface Props extends ChildrenProp, ClassNameProp, ThemeProp {
  type?: "button" | "submit" | "reset";
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
}

const THEME_CLASSNAMES = {
  base: "px-3 py-2 border bg-white text-black",
  primary: "px-3 py-2 border bg-green text-white",
};

export default function Button({
  children,
  className = "",
  type = "button",
  onClick,
  theme = "base",
}: Props) {
  return (
    <button
      className={`${className} ${THEME_CLASSNAMES[theme]}`}
      type={type}
      onClick={onClick && onClick}
    >
      {children}
    </button>
  );
}
