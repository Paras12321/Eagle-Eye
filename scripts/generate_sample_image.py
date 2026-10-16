"""Script to generate a synthetic industrial control cabinet photograph for EAGLE EYE demo.

Produces a clean, realistic industrial control cabinet graphic with DIN rails,
circuit breaker Q1, 24V power supply, PLC controller, terminal strip, and ground bus.
Zero proprietary or confidential data.
"""

from pathlib import Path
import cv2
import numpy as np

def generate_sample_cabinet_image(output_path: Path):
    width, height = 960, 680
    # Industrial cabinet interior: light neutral enclosure backplane
    img = np.full((height, width, 3), (215, 218, 222), dtype=np.uint8)

    # Outer cabinet frame (dark gray metallic border)
    cv2.rectangle(img, (20, 20), (width - 20, height - 20), (70, 75, 80), 8)
    cv2.rectangle(img, (28, 28), (width - 28, height - 28), (140, 145, 150), 3)

    # DIN Rail 1 (Top)
    rail1_y1, rail1_y2 = 210, 250
    cv2.rectangle(img, (60, rail1_y1), (width - 60, rail1_y2), (170, 175, 180), -1)
    cv2.rectangle(img, (60, rail1_y1), (width - 60, rail1_y2), (120, 125, 130), 2)
    # DIN rail slots
    for sx in range(80, width - 80, 40):
        cv2.rectangle(img, (sx, rail1_y1 + 14), (sx + 20, rail1_y2 - 14), (130, 135, 140), -1)

    # DIN Rail 2 (Bottom)
    rail2_y1, rail2_y2 = 450, 490
    cv2.rectangle(img, (60, rail2_y1), (width - 60, rail2_y2), (170, 175, 180), -1)
    cv2.rectangle(img, (60, rail2_y1), (width - 60, rail2_y2), (120, 125, 130), 2)
    for sx in range(80, width - 80, 40):
        cv2.rectangle(img, (sx, rail2_y1 + 14), (sx + 20, rail2_y2 - 14), (130, 135, 140), -1)

    # Vertical wire duct (left and right)
    cv2.rectangle(img, (40, 50), (120, height - 50), (90, 95, 100), -1)
    cv2.rectangle(img, (width - 120, 50), (width - 40, height - 50), (90, 95, 100), -1)
    for slot_y in range(70, height - 70, 30):
        cv2.rectangle(img, (45, slot_y), (115, slot_y + 12), (60, 65, 70), -1)
        cv2.rectangle(img, (width - 115, slot_y), (width - 45, slot_y + 12), (60, 65, 70), -1)

    # Top Component 1: Main Circuit Breaker Q1 (160, 140, 360, 320)
    # Box: x1=160, y1=140, x2=360, y2=320
    cv2.rectangle(img, (160, 140), (360, 320), (240, 240, 242), -1)
    cv2.rectangle(img, (160, 140), (360, 320), (50, 50, 50), 3)
    # Breaker toggles (3-pole)
    for bx in [190, 245, 300]:
        cv2.rectangle(img, (bx, 190), (bx + 30, 260), (40, 40, 40), -1)
        cv2.rectangle(img, (bx + 4, 200), (bx + 26, 230), (0, 180, 0), -1) # Green ON indicator
    cv2.putText(img, "Q1 - 63A MCB", (180, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (20, 20, 20), 2)
    cv2.putText(img, "3-POLE 400V", (190, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (80, 80, 80), 1)

    # Top Component 2: Power Supply PSU 24VDC (420, 140, 580, 320)
    # Box: x1=420, y1=140, x2=580, y2=320
    cv2.rectangle(img, (420, 140), (580, 320), (230, 230, 235), -1)
    cv2.rectangle(img, (420, 140), (580, 320), (60, 60, 60), 3)
    cv2.putText(img, "PSU 24VDC", (435, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
    cv2.circle(img, (500, 220), 12, (0, 200, 0), -1) # Green Power LED
    cv2.circle(img, (500, 220), 12, (255, 255, 255), 2)
    cv2.putText(img, "DC OK", (475, 255), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 140, 0), 1)
    cv2.putText(img, "10A OUTPUT", (445, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (80, 80, 80), 1)

    # Top Component 3: PLC Controller (640, 140, 840, 320)
    # Box: x1=640, y1=140, x2=840, y2=320
    cv2.rectangle(img, (640, 140), (840, 320), (50, 55, 60), -1)
    cv2.rectangle(img, (640, 140), (840, 320), (30, 30, 30), 3)
    cv2.putText(img, "CPU-314 PLC", (660, 170), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (240, 240, 240), 2)
    # Status LED
    cv2.circle(img, (680, 210), 8, (0, 220, 0), -1) # RUN LED green
    cv2.putText(img, "RUN", (700, 215), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)
    cv2.circle(img, (680, 240), 8, (40, 40, 40), -1) # STOP LED off
    cv2.putText(img, "STOP", (700, 245), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (120, 120, 120), 1)
    # I/O connector block
    cv2.rectangle(img, (660, 265), (820, 305), (100, 105, 110), -1)
    for i in range(8):
        cv2.circle(img, (675 + i * 18, 285), 4, (30, 30, 30), -1)

    # Bottom Component 1: Terminal Strip TB-01 to TB-12 (160, 420, 520, 520)
    # Box: x1=160, y1=420, x2=520, y2=520
    cv2.rectangle(img, (160, 420), (520, 520), (180, 185, 190), -1)
    cv2.rectangle(img, (160, 420), (520, 520), (50, 50, 50), 2)
    for t_idx in range(12):
        tx = 160 + t_idx * 30
        cv2.rectangle(img, (tx, 420), (tx + 28, 520), (195, 200, 205), -1)
        cv2.rectangle(img, (tx, 420), (tx + 28, 520), (100, 105, 110), 1)
        # Screw terminal
        cv2.circle(img, (tx + 14, 440), 5, (60, 60, 60), -1)
        cv2.circle(img, (tx + 14, 500), 5, (60, 60, 60), -1)
        # Label
        lbl = f"{t_idx + 1:02d}"
        cv2.putText(img, lbl, (tx + 4, 475), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (30, 30, 30), 1)

    # Glare / lighting reflection over terminals 7-9 (simulating optical ambiguity)
    glare_overlay = img.copy()
    cv2.ellipse(glare_overlay, (390, 470), (70, 35), 25, 0, 360, (255, 255, 255), -1)
    cv2.addWeighted(glare_overlay, 0.45, img, 0.55, 0, img)
    # Re-stroke terminal box
    cv2.rectangle(img, (160, 420), (520, 520), (50, 50, 50), 2)
    cv2.putText(img, "TB-01..12 STRIP", (180, 410), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (30, 30, 30), 1)

    # Bottom Component 2: Safety Ground PE Busbar (620, 440, 800, 540)
    # Box: x1=620, y1=440, x2=800, y2=540
    cv2.rectangle(img, (620, 440), (800, 540), (190, 180, 140), -1) # Brass/copper busbar
    cv2.rectangle(img, (620, 440), (800, 540), (80, 70, 40), 2)
    cv2.putText(img, "PE GROUND BUS", (635, 432), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (30, 80, 30), 2)
    # Screws
    for gx in [650, 710, 770]:
        cv2.circle(img, (gx, 490), 8, (60, 50, 30), -1)
        cv2.line(img, (gx - 5, 490), (gx + 5, 490), (140, 130, 100), 2)
    # Disconnected wire lug hanging loose
    # Green-yellow wire segment
    cv2.line(img, (620, 530), (670, 520), (0, 200, 0), 6)
    cv2.line(img, (620, 530), (670, 520), (0, 230, 230), 2) # Yellow stripe
    # Loose disconnected ring terminal lug
    cv2.circle(img, (675, 520), 9, (180, 180, 185), -1)
    cv2.circle(img, (675, 520), 4, (100, 100, 105), -1)
    cv2.putText(img, "DISCONNECTED", (640, 560), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 200), 1)

    # Nameplate / Cabinet Label
    cv2.rectangle(img, (380, 40), (580, 85), (250, 250, 250), -1)
    cv2.rectangle(img, (380, 40), (580, 85), (40, 40, 40), 2)
    cv2.putText(img, "PANEL-A101 [DEMO]", (395, 65), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (20, 20, 20), 2)
    cv2.putText(img, "EAGLE EYE QC TEST", (420, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (100, 100, 100), 1)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(output_path), img)
    print(f"Generated sample cabinet image at: {output_path}")

if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "sample_data" / "sample_cabinet.png"
    generate_sample_cabinet_image(out)
