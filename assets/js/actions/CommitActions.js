import * as types from './ActionTypes';

export const createRepositorySuccess = (response, errorMessages) => ({
  type: types.CREATE_REPOSITORY_SUCCESS,
  payload: { response, errorMessages },
});

export const getRepositorySuccess = (repositories) => ({
  type: types.GET_REPOSITORY_SUCCESS,
  payload: repositories,
});

export const getCommitsSuccess = (commits) => ({
  type: types.GET_COMMITS_SUCCESS,
  payload: commits,
});
