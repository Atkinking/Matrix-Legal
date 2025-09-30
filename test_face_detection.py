#!/usr/bin/env python3
"""
Test ansiktsdetektering på din bild
"""

import cv2
import numpy as np
import os

def test_face_detection(image_path):
    """Test ansiktsdetektering"""
    print(f"🔍 Testar ansiktsdetektering på: {image_path}")
    
    # Ladda bild
    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ Kunde inte ladda bild: {image_path}")
        return
    
    print(f"✅ Bild laddad: {image.shape}")
    
    # Konvertera till gråskala
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Ladda Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detektera ansikten
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    
    print(f"🎯 Detekterade {len(faces)} ansikten")
    
    # Visa resultat
    for i, (x, y, w, h) in enumerate(faces):
        print(f"   Ansikte {i+1}: Position ({x}, {y}), Storlek ({w}, {h})")
        
        # Rita ruta runt ansiktet
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    # Spara resultatbild
    output_path = "face_detection_result.jpg"
    cv2.imwrite(output_path, image)
    print(f"💾 Resultat sparat som: {output_path}")
    
    return len(faces)

if __name__ == "__main__":
    image_path = "D9F84E77-7009-4702-8DC1-0CA72FEFCF9E.P.jpg"
    test_face_detection(image_path)
