import { combineReducers } from 'redux';
import { reducer as formReducer } from 'redux-form';

// Reducers
import commitReducer from './CommitReducer';

// Combine Reducers
const reducers = combineReducers({
  form: formReducer,
  commitState: commitReducer,
});

export default reducers;
