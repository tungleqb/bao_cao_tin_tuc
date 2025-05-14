import React from "react";

const Sidebar = ({ periods, selectedPeriod, onSelectPeriod }) => {
  return (
    <div className="w-1/5 bg-white border-r p-4">
      <h2 className="text-lg font-bold mb-4">Kỳ báo cáo</h2>
      <ul className="space-y-2">
        {periods.map((p) => (
          <li
            key={p.ID}
            onClick={() => onSelectPeriod(p)}
            className={`cursor-pointer p-2 rounded hover:bg-blue-100 ${
              selectedPeriod?.ID === p.ID ? "bg-blue-500 text-white" : ""
            }`}
          >
            <div className="font-semibold">{p.Name}</div>
            <div className="text-sm text-gray-600">
              {new Date(p.StartAt).toLocaleDateString()} - {new Date(p.EndAt).toLocaleDateString()}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;
