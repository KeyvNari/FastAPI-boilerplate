#!/bin/bash

# TimerSync API Test Script
# This script tests all major endpoints of the TimerSync API

# Configuration
BASE_URL="http://localhost:8000"  # Change this to your API base URL
API_VERSION="/api/v1"
FULL_URL="${BASE_URL}${API_VERSION}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Global variables for storing tokens and IDs
ACCESS_TOKEN=""
REFRESH_TOKEN=""
USER_ID=""
USERNAME=""
TIER_ID=""
POST_ID=""
ROOM_ID=""
RATE_LIMIT_ID=""

# Helper function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}[INFO]${NC} $message"
            ;;
        "SUCCESS")
            echo -e "${GREEN}[SUCCESS]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
        "WARNING")
            echo -e "${YELLOW}[WARNING]${NC} $message"
            ;;
    esac
}

# Helper function to make API calls
api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    local auth_header=$4
    local content_type=${5:-"application/json"}
    
    local curl_cmd="curl -s -X $method"
    
    if [ ! -z "$auth_header" ]; then
        curl_cmd="$curl_cmd -H 'Authorization: Bearer $ACCESS_TOKEN'"
    fi
    
    if [ ! -z "$data" ]; then
        curl_cmd="$curl_cmd -H 'Content-Type: $content_type' -d '$data'"
    fi
    
    curl_cmd="$curl_cmd ${FULL_URL}$endpoint"
    
    eval $curl_cmd
}

# Test user registration
test_user_registration() {
    print_status "INFO" "Testing user registration..."
    
    local test_user_data='{
        "name": "Test User",
        "username": "testuser123",
        "email": "test@example.com",
        "password": "TestPass123!"
    }'
    
    local response=$(api_call "POST" "/user" "$test_user_data")
    
    if echo "$response" | grep -q '"id"'; then
        USER_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d: -f2)
        USERNAME=$(echo "$response" | grep -o '"username":"[^"]*"' | cut -d: -f2 | tr -d '"')
        print_status "SUCCESS" "User registered successfully. ID: $USER_ID, Username: $USERNAME"
        echo "Response: $response"
    else
        print_status "ERROR" "User registration failed"
        echo "Response: $response"
        return 1
    fi
}

# Test user login
test_user_login() {
    print_status "INFO" "Testing user login..."
    
    local login_data="username=testuser123&password=TestPass123!"
    
    local response=$(api_call "POST" "/login" "$login_data" "" "application/x-www-form-urlencoded")
    
    if echo "$response" | grep -q '"access_token"'; then
        ACCESS_TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*"' | cut -d: -f2 | tr -d '"')
        print_status "SUCCESS" "Login successful"
        echo "Access token obtained: ${ACCESS_TOKEN:0:20}..."
    else
        print_status "ERROR" "Login failed"
        echo "Response: $response"
        return 1
    fi
}

# Test get current user
test_get_current_user() {
    print_status "INFO" "Testing get current user..."
    
    local response=$(api_call "GET" "/user/me/" "" "true")
    
    if echo "$response" | grep -q '"username"'; then
        print_status "SUCCESS" "Current user retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get current user"
        echo "Response: $response"
    fi
}

# Test get all users
test_get_users() {
    print_status "INFO" "Testing get all users..."
    
    local response=$(api_call "GET" "/users?page=1&items_per_page=5")
    
    if echo "$response" | grep -q '"data"'; then
        print_status "SUCCESS" "Users list retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get users list"
        echo "Response: $response"
    fi
}

# Test get specific user
test_get_user() {
    print_status "INFO" "Testing get specific user..."
    
    local response=$(api_call "GET" "/user/$USERNAME")
    
    if echo "$response" | grep -q '"username"'; then
        print_status "SUCCESS" "Specific user retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get specific user"
        echo "Response: $response"
    fi
}

# Test create tier
test_create_tier() {
    print_status "INFO" "Testing tier creation..."
    
    local tier_data='{
        "name": "test_tier"
    }'
    
    local response=$(api_call "POST" "/tier" "$tier_data" "true")
    
    if echo "$response" | grep -q '"id"'; then
        TIER_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d: -f2)
        print_status "SUCCESS" "Tier created successfully. ID: $TIER_ID"
        echo "Response: $response"
    else
        print_status "ERROR" "Tier creation failed"
        echo "Response: $response"
    fi
}

# Test get tiers
test_get_tiers() {
    print_status "INFO" "Testing get all tiers..."
    
    local response=$(api_call "GET" "/tiers")
    
    if echo "$response" | grep -q '"data"'; then
        print_status "SUCCESS" "Tiers list retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get tiers list"
        echo "Response: $response"
    fi
}

# Test create rate limit
test_create_rate_limit() {
    print_status "INFO" "Testing rate limit creation..."
    
    if [ -z "$TIER_ID" ]; then
        print_status "WARNING" "No tier ID available, skipping rate limit test"
        return
    fi
    
    local rate_limit_data='{
        "path": "test_path",
        "limit": 100,
        "period": 3600,
        "name": "test_rate_limit"
    }'
    
    local response=$(api_call "POST" "/tier/test_tier/rate_limit" "$rate_limit_data" "true")
    
    if echo "$response" | grep -q '"id"'; then
        RATE_LIMIT_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d: -f2)
        print_status "SUCCESS" "Rate limit created successfully. ID: $RATE_LIMIT_ID"
        echo "Response: $response"
    else
        print_status "ERROR" "Rate limit creation failed"
        echo "Response: $response"
    fi
}

# Test create post
test_create_post() {
    print_status "INFO" "Testing post creation..."
    
    local post_data='{
        "title": "Test Post",
        "text": "This is a test post content for API testing.",
        "media_url": "https://example.com/image.jpg"
    }'
    
    local response=$(api_call "POST" "/$USERNAME/post" "$post_data" "true")
    
    if echo "$response" | grep -q '"id"'; then
        POST_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d: -f2)
        print_status "SUCCESS" "Post created successfully. ID: $POST_ID"
        echo "Response: $response"
    else
        print_status "ERROR" "Post creation failed"
        echo "Response: $response"
    fi
}

# Test get posts
test_get_posts() {
    print_status "INFO" "Testing get user posts..."
    
    local response=$(api_call "GET" "/$USERNAME/posts?page=1&items_per_page=5")
    
    if echo "$response" | grep -q '"data"'; then
        print_status "SUCCESS" "Posts retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get posts"
        echo "Response: $response"
    fi
}

# Test get specific post
test_get_post() {
    print_status "INFO" "Testing get specific post..."
    
    if [ -z "$POST_ID" ]; then
        print_status "WARNING" "No post ID available, skipping specific post test"
        return
    fi
    
    local response=$(api_call "GET" "/$USERNAME/post/$POST_ID")
    
    if echo "$response" | grep -q '"title"'; then
        print_status "SUCCESS" "Specific post retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get specific post"
        echo "Response: $response"
    fi
}

# Test create room
test_create_room() {
    print_status "INFO" "Testing room creation..."
    
    local room_data='{
        "created_by_user_id": '$USER_ID',
        "name": "Test Room",
        "description": "This is a test room for API testing",
        "time_zone": "UTC",
        "is_active": true
    }'
    
    local response=$(api_call "POST" "/room" "$room_data" "true")
    
    if echo "$response" | grep -q '"id"'; then
        ROOM_ID=$(echo "$response" | grep -o '"id":[0-9]*' | cut -d: -f2)
        print_status "SUCCESS" "Room created successfully. ID: $ROOM_ID"
        echo "Response: $response"
    else
        print_status "ERROR" "Room creation failed"
        echo "Response: $response"
    fi
}

# Test get rooms
test_get_rooms() {
    print_status "INFO" "Testing get all rooms..."
    
    local response=$(api_call "GET" "/rooms" "" "true")
    
    if echo "$response" | grep -q '"data"'; then
        print_status "SUCCESS" "Rooms list retrieved successfully"
        echo "Response: $response"
    else
        print_status "ERROR" "Failed to get rooms list"
        echo "Response: $response"
    fi
}

# Test playback status
test_playback_status() {
    print_status "INFO" "Testing playback status..."
    
    if [ -z "$ROOM_ID" ]; then
        ROOM_ID="test_room_123"
        print_status "WARNING" "Using default room ID for playback test"
    fi
    
    # Set playback status
    local status_data='{
        "is_playing": true,
        "current_time": 120,
        "video_url": "https://example.com/video.mp4"
    }'
    
    local response=$(api_call "POST" "/playback/status/$ROOM_ID" "$status_data")
    print_status "INFO" "Set playback status response: $response"
    
    # Get playback status
    local response=$(api_call "GET" "/playback/status/$ROOM_ID")
    print_status "INFO" "Get playback status response: $response"
}

# Test room data storage
test_room_data() {
    print_status "INFO" "Testing room data storage..."
    
    if [ -z "$ROOM_ID" ]; then
        ROOM_ID="test_room_123"
    fi
    
    # Set room data
    local data='{
        "participants": ["user1", "user2"],
        "created_at": "2025-01-01T00:00:00Z"
    }'
    
    local response=$(api_call "POST" "/playback/data/$ROOM_ID/metadata" "$data")
    print_status "INFO" "Set room data response: $response"
    
    # Get room data
    local response=$(api_call "GET" "/playback/data/$ROOM_ID/metadata")
    print_status "INFO" "Get room data response: $response"
    
    # Get room keys
    local response=$(api_call "GET" "/playback/keys/$ROOM_ID")
    print_status "INFO" "Get room keys response: $response"
}

# Test task creation
test_create_task() {
    print_status "INFO" "Testing task creation..."
    
    local response=$(api_call "POST" "/tasks/task?message=test_message_123")
    
    if echo "$response" | grep -q '"id"'; then
        local task_id=$(echo "$response" | grep -o '"id":"[^"]*"' | cut -d: -f2 | tr -d '"')
        print_status "SUCCESS" "Task created successfully. ID: $task_id"
        echo "Response: $response"
        
        # Test get task
        sleep 1
        local task_response=$(api_call "GET" "/tasks/task/$task_id")
        print_status "INFO" "Get task response: $task_response"
    else
        print_status "ERROR" "Task creation failed"
        echo "Response: $response"
    fi
}

# Test token refresh
test_token_refresh() {
    print_status "INFO" "Testing token refresh..."
    
    local response=$(api_call "POST" "/refresh")
    
    if echo "$response" | grep -q 'access_token\|message'; then
        print_status "SUCCESS" "Token refresh attempted"
        echo "Response: $response"
    else
        print_status "ERROR" "Token refresh failed"
        echo "Response: $response"
    fi
}

# Test logout
test_logout() {
    print_status "INFO" "Testing logout..."
    
    local response=$(api_call "POST" "/logout" "" "true")
    
    print_status "INFO" "Logout response: $response"
}

# Main test runner
run_tests() {
    print_status "INFO" "Starting TimerSync API tests..."
    print_status "INFO" "Base URL: $FULL_URL"
    echo ""
    
    # Authentication flow
    test_user_registration
    echo ""
    
    test_user_login
    echo ""
    
    if [ -z "$ACCESS_TOKEN" ]; then
        print_status "ERROR" "Cannot proceed without access token"
        exit 1
    fi
    
    # User endpoints
    test_get_current_user
    echo ""
    
    test_get_users
    echo ""
    
    test_get_user
    echo ""
    
    # Tier endpoints
    test_create_tier
    echo ""
    
    test_get_tiers
    echo ""
    
    # Rate limit endpoints
    test_create_rate_limit
    echo ""
    
    # Post endpoints
    test_create_post
    echo ""
    
    test_get_posts
    echo ""
    
    test_get_post
    echo ""
    
    # Room endpoints
    test_create_room
    echo ""
    
    test_get_rooms
    echo ""
    
    # Playback endpoints
    test_playback_status
    echo ""
    
    test_room_data
    echo ""
    
    # Task endpoints
    test_create_task
    echo ""
    
    # Token management
    test_token_refresh
    echo ""
    
    test_logout
    echo ""
    
    print_status "SUCCESS" "All tests completed!"
}

# Help function
show_help() {
    echo "TimerSync API Test Script"
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -u, --url URL      Set the base URL (default: http://localhost:8000)"
    echo "  -h, --help         Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0                                    # Run tests against localhost:8000"
    echo "  $0 -u https://api.example.com        # Run tests against custom URL"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -u|--url)
            BASE_URL="$2"
            FULL_URL="${BASE_URL}${API_VERSION}"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_status "ERROR" "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Run the tests
run_tests