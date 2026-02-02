#!/usr/bin/env python3
"""
Doorbot Client - Raspberry Pi Door Lock Controller

This script polls the doorbot server and controls the door lock hardware.
Pre-configured for: http://newyakko.cs.wmich.edu:8878

Hardware Requirements:
- Raspberry Pi with GPIO access
- Stepper motor connected to GPIO 18 (PWM), GPIO 15 (direction)
- Power relay on GPIO 4
- Position sensor/button on GPIO 7

Usage:
    python3 doorbot_client.py

Auto-start on boot:
    See INSTALLATION.md for systemd service setup
"""

import RPi.GPIO as GPIO
import time
import requests
import json
from datetime import datetime

# ============================================================================
# CONFIGURATION - Change these values if needed
# ============================================================================

# Server Configuration
SERVER_URL = "http://newyakko.cs.wmich.edu:8878"
POLL_INTERVAL = 1.0  # seconds between server polls

# GPIO Pin Configuration
RELAY_PIN = 4        # Power relay control
DIRECTION_PIN = 15   # Motor direction control
PWM_PIN = 18         # Stepper motor PWM
BUTTON_PIN = 7       # Position sensor/button

# Motor Configuration
PWM_FREQUENCY = 500  # Hz
MOTOR_DUTY_CYCLE = 50  # Percent
UNLOCK_HOLD_TIME = 10  # seconds to hold door unlocked

# ============================================================================
# SETUP
# ============================================================================

def setup_gpio():
    """Initialize GPIO pins for hardware control"""
    print(f"[{get_timestamp()}] Initializing GPIO pins...")

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Set up output pins
    GPIO.setup(RELAY_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(DIRECTION_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(PWM_PIN, GPIO.OUT)

    # Set up input pin (position sensor)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Initialize PWM
    pwm = GPIO.PWM(PWM_PIN, PWM_FREQUENCY)

    print(f"[{get_timestamp()}] GPIO initialization complete")
    print(f"  - Relay: GPIO {RELAY_PIN}")
    print(f"  - Direction: GPIO {DIRECTION_PIN}")
    print(f"  - PWM Motor: GPIO {PWM_PIN}")
    print(f"  - Position Sensor: GPIO {BUTTON_PIN}")

    return pwm

def get_timestamp():
    """Get current timestamp string"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ============================================================================
# DOOR CONTROL FUNCTIONS
# ============================================================================

def unlock_door(pwm):
    """
    Execute the door unlock sequence:
    1. Activate motor to turn handle
    2. Wait for position sensor to detect unlock position
    3. Hold for UNLOCK_HOLD_TIME seconds
    4. Return handle to locked position
    """
    print(f"\n{'='*60}")
    print(f"[{get_timestamp()}] 🔓 UNLOCKING DOOR")
    print(f"{'='*60}")

    try:
        # Step 1: Activate relay (power on)
        print(f"[{get_timestamp()}] Activating power relay...")
        GPIO.output(RELAY_PIN, GPIO.HIGH)
        time.sleep(0.5)

        # Step 2: Set direction and start motor
        print(f"[{get_timestamp()}] Starting motor (unlock direction)...")
        GPIO.output(DIRECTION_PIN, GPIO.HIGH)
        pwm.start(MOTOR_DUTY_CYCLE)

        # Step 3: Wait for position sensor
        print(f"[{get_timestamp()}] Waiting for unlock position...")
        timeout = 10  # Maximum wait time
        start_time = time.time()

        while GPIO.input(BUTTON_PIN) == GPIO.HIGH:  # Button not pressed
            if time.time() - start_time > timeout:
                print(f"[{get_timestamp()}] ⚠️  WARNING: Position sensor timeout!")
                break
            time.sleep(0.1)

        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print(f"[{get_timestamp()}] ✓ Unlock position reached!")

        # Step 4: Stop motor
        pwm.stop()

        # Step 5: Hold unlocked position
        print(f"[{get_timestamp()}] Holding unlocked for {UNLOCK_HOLD_TIME} seconds...")
        time.sleep(UNLOCK_HOLD_TIME)

        # Step 6: Return to locked position
        print(f"[{get_timestamp()}] Returning to locked position...")
        GPIO.output(DIRECTION_PIN, GPIO.LOW)  # Reverse direction
        pwm.start(MOTOR_DUTY_CYCLE)

        # Wait for return (or timeout)
        start_time = time.time()
        while GPIO.input(BUTTON_PIN) == GPIO.LOW:  # Button still pressed
            if time.time() - start_time > timeout:
                break
            time.sleep(0.1)

        pwm.stop()

        # Step 7: Power off
        print(f"[{get_timestamp()}] Deactivating power relay...")
        GPIO.output(RELAY_PIN, GPIO.LOW)

        print(f"[{get_timestamp()}] ✓ Door lock sequence complete")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"[{get_timestamp()}] ❌ ERROR during unlock: {e}")
        # Safety: ensure motor is stopped and power is off
        pwm.stop()
        GPIO.output(RELAY_PIN, GPIO.LOW)
        raise

# ============================================================================
# SERVER COMMUNICATION
# ============================================================================

def poll_server():
    """
    Poll the server for unlock commands

    Returns:
        dict: Server response with 'letmein' status, or None if error
    """
    try:
        response = requests.get(SERVER_URL, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data

    except requests.exceptions.ConnectionError:
        print(f"[{get_timestamp()}] ⚠️  Cannot connect to server: {SERVER_URL}")
        return None

    except requests.exceptions.Timeout:
        print(f"[{get_timestamp()}] ⚠️  Server timeout")
        return None

    except requests.exceptions.RequestException as e:
        print(f"[{get_timestamp()}] ⚠️  Server error: {e}")
        return None

    except json.JSONDecodeError:
        print(f"[{get_timestamp()}] ⚠️  Invalid JSON response from server")
        return None

# ============================================================================
# MAIN LOOP
# ============================================================================

def main():
    """Main program loop"""

    print("\n" + "="*60)
    print("🚪 DOORBOT CLIENT")
    print("="*60)
    print(f"Server: {SERVER_URL}")
    print(f"Poll Interval: {POLL_INTERVAL}s")
    print(f"Started: {get_timestamp()}")
    print("="*60 + "\n")

    # Initialize hardware
    pwm = setup_gpio()

    print(f"\n[{get_timestamp()}] Starting server polling...")
    print(f"[{get_timestamp()}] Press Ctrl+C to stop\n")

    consecutive_errors = 0
    max_consecutive_errors = 10

    try:
        while True:
            # Poll server
            status = poll_server()

            if status is None:
                consecutive_errors += 1
                if consecutive_errors >= max_consecutive_errors:
                    print(f"[{get_timestamp()}] ❌ Too many consecutive errors. Stopping.")
                    break
                time.sleep(POLL_INTERVAL)
                continue

            # Reset error counter on success
            consecutive_errors = 0

            # Check if unlock is requested
            if status.get('letmein', False):
                unlock_door(pwm)
            else:
                # Quiet waiting (only show dots every 10 polls)
                pass

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print(f"\n[{get_timestamp()}] Received shutdown signal")

    except Exception as e:
        print(f"\n[{get_timestamp()}] ❌ Fatal error: {e}")

    finally:
        # Cleanup
        print(f"[{get_timestamp()}] Cleaning up GPIO...")
        pwm.stop()
        GPIO.output(RELAY_PIN, GPIO.LOW)
        GPIO.cleanup()
        print(f"[{get_timestamp()}] Shutdown complete")
        print("="*60 + "\n")

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
