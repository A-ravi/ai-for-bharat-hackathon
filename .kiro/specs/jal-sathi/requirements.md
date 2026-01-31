# Requirements Document

## Introduction

Jal Sathi (जल साथी - "Water Companion") is an AI-powered irrigation advisor platform designed to help Indian farmers optimize water usage and reduce irrigation costs. The system provides personalized guidance in regional Indian languages through a responsive web application and SMS to achieve 30-40% water savings and significant cost reductions for small and medium farmers.

## Glossary

- **Jal_Sathi**: The AI-powered irrigation advisor platform
- **Farmer**: Primary user who owns or manages agricultural land (2-20 acres)
- **Field**: A specific agricultural plot with defined crop, location, and irrigation system
- **Irrigation_Recommendation**: Daily advice on whether to irrigate, how much water to apply, and optimal timing
- **Schedule**: 7-day irrigation plan showing when and how much to irrigate
- **Savings_Tracker**: Component that calculates and displays water and cost savings compared to traditional methods
- **SMS_Service**: Text message delivery system for irrigation alerts
- **Weather_API**: External service providing weather data and forecasts
- **Satellite_API**: External service providing soil moisture and crop health data

## Requirements

### Requirement 1: Regional Language Onboarding

**User Story:** As a farmer, I want to set up my field profile in my preferred regional language through simple questions, so that I can receive personalized irrigation advice in a language I understand.

#### Acceptance Criteria

1. WHEN a new farmer opens the app, THE Jal_Sathi SHALL display an onboarding flow in the farmer's selected regional language
2. THE Jal_Sathi SHALL support major Indian languages including Hindi, English, Marathi, Gujarati, Punjabi, Tamil, Telugu, and Kannada
3. THE Jal_Sathi SHALL collect exactly 5 pieces of information: crop type, field size, location, irrigation method, and contact number
4. WHEN a farmer selects a crop type, THE Jal_Sathi SHALL provide options in the selected language with common regional crops
5. WHEN a farmer enters field size, THE Jal_Sathi SHALL accept input in acres and validate it is between 0.1 and 50 acres
6. WHEN a farmer provides location, THE Jal_Sathi SHALL accept either GPS coordinates or manual pin code entry
7. WHEN onboarding is complete, THE Jal_Sathi SHALL create a field profile and immediately generate the first irrigation recommendation

### Requirement 2: Daily Irrigation Recommendations

**User Story:** As a farmer, I want to receive daily irrigation advice in my regional language, so that I know exactly when and how much to water my crops.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL generate daily irrigation recommendations by 6 AM local time
2. WHEN displaying recommendations, THE Jal_Sathi SHALL show three key pieces of information: whether to irrigate (yes/no), water amount in millimeters, and optimal timing
3. WHEN recommending irrigation, THE Jal_Sathi SHALL provide the advice in the farmer's selected regional language with simple agricultural terminology
4. WHEN no irrigation is needed, THE Jal_Sathi SHALL display appropriate messaging in the selected language with explanation
5. THE Jal_Sathi SHALL base recommendations on weather forecast, soil moisture, crop stage, and historical irrigation patterns
6. WHEN weather conditions change significantly, THE Jal_Sathi SHALL update recommendations and notify the farmer

### Requirement 3: 7-Day Irrigation Schedule

**User Story:** As a farmer, I want to see a weekly irrigation plan, so that I can prepare my irrigation activities in advance.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL display a visual 7-day calendar showing planned irrigation days
2. WHEN displaying the schedule, THE Jal_Sathi SHALL show water amount and timing for each irrigation day
3. THE Jal_Sathi SHALL use clear visual indicators: green for irrigation days, gray for no-irrigation days
4. WHEN a farmer taps on a specific day, THE Jal_Sathi SHALL show detailed information including weather forecast and reasoning
5. THE Jal_Sathi SHALL update the schedule daily based on latest weather and field conditions
6. WHEN schedule changes significantly, THE Jal_Sathi SHALL highlight the changes and explain the reason

### Requirement 4: Savings Tracking

**User Story:** As a farmer, I want to track my water and cost savings, so that I can see the financial benefits of using Jal Sathi.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL calculate water savings by comparing recommended irrigation with traditional over-watering patterns
2. THE Jal_Sathi SHALL calculate cost savings using local water rates (₹2-5 per 1000 liters)
3. WHEN displaying savings, THE Jal_Sathi SHALL show both water saved (in liters) and money saved (in rupees)
4. THE Jal_Sathi SHALL display cumulative savings with encouraging messages in the farmer's selected language
5. THE Jal_Sathi SHALL show savings comparison with visual progress bars or charts
6. WHEN savings reach significant milestones, THE Jal_Sathi SHALL celebrate with congratulatory messages

### Requirement 5: SMS Alert System

**User Story:** As a farmer, I want to receive irrigation advice via SMS, so that I can get recommendations even when I don't have smartphone access or internet connectivity.

#### Acceptance Criteria

1. WHEN daily recommendations are generated, THE SMS_Service SHALL send a text message to the farmer's registered mobile number
2. THE SMS_Service SHALL format messages in the farmer's preferred regional language within 160 characters for single SMS delivery
3. WHEN urgent irrigation is needed due to weather changes, THE SMS_Service SHALL send immediate alerts
4. THE SMS_Service SHALL include essential information: irrigation decision, water amount, and timing
5. WHEN farmers reply with status updates, THE SMS_Service SHALL process and store the feedback
6. THE SMS_Service SHALL handle delivery failures gracefully and retry up to 3 times

### Requirement 6: Weather Integration

**User Story:** As a system administrator, I want to integrate real-time weather data, so that irrigation recommendations are based on accurate meteorological information.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL fetch weather data from reliable Indian meteorological services
2. WHEN processing weather data, THE Jal_Sathi SHALL consider temperature, humidity, rainfall, wind speed, and forecast accuracy
3. THE Jal_Sathi SHALL update weather data every 6 hours to ensure recommendation accuracy
4. WHEN weather API is unavailable, THE Jal_Sathi SHALL use cached data and notify users of potential inaccuracy
5. THE Jal_Sathi SHALL prioritize local weather stations within 50km of the farmer's location
6. WHEN extreme weather is predicted, THE Jal_Sathi SHALL issue special advisories and modify irrigation schedules

### Requirement 7: Data Persistence and Sync

**User Story:** As a farmer, I want my field data and irrigation history to be saved reliably, so that I don't lose my information and can access it across devices.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL store all farmer profiles, field data, and irrigation history in a persistent database
2. WHEN farmers log irrigation activities, THE Jal_Sathi SHALL immediately save the data with timestamps
3. THE Jal_Sathi SHALL sync data across mobile app and SMS interfaces
4. WHEN network connectivity is poor, THE Jal_Sathi SHALL cache data locally and sync when connection is restored
5. THE Jal_Sathi SHALL backup critical data daily to prevent data loss
6. WHEN farmers switch devices, THE Jal_Sathi SHALL allow data recovery using mobile number verification

### Requirement 8: Web Application Interface

**User Story:** As a farmer, I want a simple and intuitive web application interface in my regional language, so that I can easily access irrigation advice and manage my field information from any device with internet access.

#### Acceptance Criteria

1. THE Jal_Sathi SHALL provide a responsive web application interface that works on desktop, tablet, and mobile browsers
2. WHEN farmers open the web app, THE Jal_Sathi SHALL display the main dashboard with today's recommendation prominently
3. THE Jal_Sathi SHALL use large, clear fonts and high-contrast colors suitable for various screen sizes and lighting conditions
4. WHEN farmers navigate the web app, THE Jal_Sathi SHALL provide all text in the farmer's selected regional language with simple, agricultural terminology
5. THE Jal_Sathi SHALL work efficiently on low-bandwidth internet connections common in rural areas
6. WHEN internet connectivity is intermittent, THE Jal_Sathi SHALL show cached recommendations and indicate data freshness