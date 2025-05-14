import React from "react";

const ReportForm = ({ period }) => {
  return (
    <div className="bg-white p-6 rounded shadow">
      <h2 className="text-lg font-semibold mb-4">Gửi báo cáo: {period.Name}</h2>
      {/* TODO: Thêm form gửi báo cáo */}
      <p>Form gửi báo cáo sẽ được hiển thị ở đây.</p>
    </div>
  );
};

export default ReportForm;
