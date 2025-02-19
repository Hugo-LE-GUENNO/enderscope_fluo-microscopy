```mermaid
graph TB
    %% Main Components
    Panel["Panel UI Interface"]
    Stage["Stage Controller<br>/dev/ttyUSB1"]
    
    %% Input Components
    subgraph Input["Input Settings"]
        Camera["EnderPiCam<br>(HQ-CAM)"]
        LightFluo["EnderPiLight<br>(Fluorescent)"]
        LightAmb["EnderPiLight<br>(Ambient)"]
        Acqui["EnderAcquisition<br>(Multi-acquisition)"]
    end
    
    %% Output Components
    subgraph Output["Output Settings"]
        CamOut["Camera Output Tab"]
    end
    
    Panel --> Stage
    Stage --> Camera
    Camera --> CamOut
    Panel --> Input
    Input --> Output
    LightFluo -.->|"Pin D18"| HW1["LED Control<br>(0-1 pixels)"]
    LightAmb -.->|"Pin D12"| HW2["LED Control<br>(0-9 pixels)"]
    Acqui --> Camera
    Acqui --> LightFluo
    Acqui --> LightAmb