import axios from 'axios';
import { reset } from 'redux-form';
import store from '../store';
import {
  getCommitsSuccess, getRepositorySuccess, createRepositorySuccess,
} from '../actions/CommitActions';

export const getCommits = (params) => {
  const getParams = Object.keys(params).length ? params : { page: 1 };

  return axios.get('/api/commits/', { params: getParams })
    .then((response) => {
      store.dispatch(getCommitsSuccess({
        ...response.data,
        params: Object.fromEntries(
          [
            ...(new URL(response.request.responseURL)).searchParams.entries(),
          ],
        ),
      }));
    });
};

export const getRepositories = () => axios.get('/api/repositories/')
  .then((response) => {
    store.dispatch(getRepositorySuccess({ ...response.data }));
  });

export const createRepository = (
  values, headers, formDispatch,
) => axios.post('/api/repositories/', values, { headers })
  .then((response) => {
    store.dispatch(createRepositorySuccess(response.data, false));
    formDispatch(reset('repoCreate'));
  }).catch(({ response }) => {
    const errors = Array.prototype.concat.apply([], Object.values(response.data));
    store.dispatch(createRepositorySuccess(response.data, errors));
    // formDispatch(reset('repoCreate'));
  });
