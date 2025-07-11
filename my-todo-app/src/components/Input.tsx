import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
}

const Input: React.FC<InputProps> = ({ value, onChange, placeholder, ...rest }) => {
  return (
    <input
      type="text"
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      {...rest}
      style={{
        padding: "8px",
        fontSize: "16px",
        width: "100%",
        boxSizing: "border-box",
      }}
    />
  );
};

export default Input;
