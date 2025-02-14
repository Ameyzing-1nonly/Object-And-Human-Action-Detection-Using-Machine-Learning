import React from 'react';
import { CameraIcon, ImageIcon, FileVideo, Video } from 'lucide-react';

function Dashboard() {
  // ✅ Fix: Define `handleFileSelect`
  const handleFileSelect = async (event, script) => {
    const file = event.target.files[0];
    if (!file) {
      alert("No file selected!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(`http://127.0.0.1:5000/run/${script}`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      alert(result.message || result.error);
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Error: Unable to connect to the server.");
    }
  };

  // ✅ Fix: Define `runLiveScript`
  const runLiveScript = async (script) => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/run/${script}`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }

      const result = await response.json();
      alert(result.message || result.error);
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Error: Unable to connect to the server.");
    }
  };

  return (
    <div className="flex justify-center items min-h-screen">
      <div className="flex justify-center gap-x-16 flex-nowrap">
        
        {/* Box 1 - Image Detection (Runs main.py) */}
        <label className="p-14 border items-center flex justify-center bg-secondary rounded-lg h-[250px] w-[250px] hover:scale-105 transition-all hover:shadow-md cursor-pointer border-dashed">
          <input type="file" accept="image/*" hidden onChange={(e) => handleFileSelect(e, "main")} />
          <ImageIcon size={50} />
        </label>

        {/* Box 2 - Live Object Detection (Runs main1.py) */}
        <div
          className="p-14 border items-center flex justify-center bg-secondary rounded-lg h-[250px] w-[250px] hover:scale-105 transition-all hover:shadow-md cursor-pointer border-dashed"
          onClick={() => runLiveScript("main1")}
        >
          <CameraIcon size={50} />
        </div>

        {/* Box 3 - Video Analysis (Runs video_analysis.py) */}
        <label className="p-14 border items-center flex justify-center bg-secondary rounded-lg h-[250px] w-[250px] hover:scale-105 transition-all hover:shadow-md cursor-pointer border-dashed">
          <input type="file" accept="video/*" hidden onChange={(e) => handleFileSelect(e, "video_analysis")} />
          <FileVideo size={50} />
        </label>

        {/* Box 4 - Live Action Recognition (Runs live_analysis.py) */}
        <div
          className="p-14 border items-center flex justify-center bg-secondary rounded-lg h-[250px] w-[250px] hover:scale-105 transition-all hover:shadow-md cursor-pointer border-dashed"
          onClick={() => runLiveScript("live_analysis")}
        >
          <Video size={50} />
        </div>

      </div>
    </div>
  );
}

export default Dashboard;
