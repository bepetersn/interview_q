/**
 * Application constants
 * @fileoverview Central location for application-wide constants
 */

/**
 * Available question sources
 * @type {string[]}
 */
export const QUESTION_SOURCES = [
  "CodeWars",
  "LeetCode",
  "HackerRank",
  "Other"
];

/**
 * Question difficulty levels
 * @type {string[]}
 */
export const DIFFICULTY_LEVELS = [
  "Easy",
  "Medium",
  "Hard"
];

/**
 * Question log outcomes
 * @type {string[]}
 */
export const LOG_OUTCOMES = [
  "Solved",
  "Partial",
  "Failed"
];

/**
 * Default form values
 */
export const DEFAULT_FORM_VALUES = {
  difficulty: "Easy",
  source: QUESTION_SOURCES[0],
  is_active: true,
  tag_ids: [],
};

/**
 * API endpoints
 */
export const API_ENDPOINTS = {
  questions: 'questions/',
  tags: 'tags/',
  questionLogs: 'question-logs/',
  auth: {
    login: 'auth/login/',
    register: 'auth/register/',
    logout: 'auth/logout/',
  }
};
