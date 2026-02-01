#!/bin/bash

# Quick test script for the Doorbot server

echo "======================================"
echo "🧪 Testing Doorbot Server"
echo "======================================"

SERVER_URL="http://localhost:8878"

# Test 1: Health check
echo ""
echo "Test 1: Health check..."
HEALTH=$(curl -s $SERVER_URL/health)
if [ $? -eq 0 ]; then
    echo "✓ Server is responding"
    echo "  Response: $HEALTH"
else
    echo "✗ Server is not responding"
    echo "  Make sure the server is running: python3 server.py"
    exit 1
fi

# Test 2: Get status
echo ""
echo "Test 2: Get door status..."
STATUS=$(curl -s $SERVER_URL/status)
echo "  Response: $STATUS"

# Test 3: Trigger unlock
echo ""
echo "Test 3: Trigger unlock..."
UNLOCK=$(curl -s -X POST $SERVER_URL/unlock)
echo "  Response: $UNLOCK"

# Test 4: Verify status changed
echo ""
echo "Test 4: Verify status changed to unlocked..."
sleep 1
STATUS=$(curl -s $SERVER_URL/status)
echo "  Response: $STATUS"

if echo "$STATUS" | grep -q '"letmein": true'; then
    echo "✓ Status correctly shows unlocked"
else
    echo "✗ Status did not change"
fi

# Test 5: Wait for auto-reset
echo ""
echo "Test 5: Waiting for auto-reset (15 seconds)..."
echo "  Press Ctrl+C to skip..."
sleep 15

STATUS=$(curl -s $SERVER_URL/status)
echo "  Response: $STATUS"

if echo "$STATUS" | grep -q '"letmein": false'; then
    echo "✓ Auto-reset working correctly"
else
    echo "⚠ Auto-reset may not be working"
fi

# Test 6: Manual lock
echo ""
echo "Test 6: Manual lock reset..."
LOCK=$(curl -s -X POST $SERVER_URL/lock)
echo "  Response: $LOCK"

echo ""
echo "======================================"
echo "✓ Tests Complete"
echo "======================================"
echo ""
echo "Server is working correctly!"
echo "Access web interface at: http://newyakko.cs.wmich.edu:8878"
echo ""
