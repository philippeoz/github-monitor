import * as types from '../actions/ActionTypes';

const initialState = {
  commits: [],
  commits_pagination: {},
  params: { page: '1' },

  repositories: [],
  repositories_pagination: {},

  errorMessages: null,
};

const commitReducer = (state = initialState, action) => {
  switch (action.type) {
    case types.GET_COMMITS_SUCCESS:
      return {
        ...state,
        commits: action.payload.results,
        params: action.payload.params,
        commits_pagination: {
          next: action.payload.next && (
            new URL(action.payload.next)
          ).searchParams.get('page'),
          previous: (
            action.payload.previous && (
              new URL(action.payload.previous)).searchParams.get('page')
          ) || (action.payload.previous && '1'),
          count: action.payload.count,
        },
      };
    case types.GET_REPOSITORY_SUCCESS:
      return {
        ...state,
        repositories: action.payload.results,
        repositories_pagination: {
          next: action.payload.next,
          previous: action.payload.previous,
          count: action.payload.count,
        },
      };
    case types.CREATE_REPOSITORY_SUCCESS: {
      return { ...state, errorMessages: action.payload.errorMessages };
    }
    default:
      return state;
  }
};

export default commitReducer;
