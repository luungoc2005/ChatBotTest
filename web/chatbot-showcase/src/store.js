import {createStore, applyMiddleware, compose} from 'redux';
import createSagaMiddleware from 'redux-saga';

import {createReducer} from './rootReducer';
import {rootSaga} from './rootSaga';

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;

export function configureStore(initialState = {}) {
  const sagaMiddleware = createSagaMiddleware();
  const store = createStore(
    createReducer(),
    initialState,
    composeEnhancers(
      applyMiddleware(sagaMiddleware)
    )
  );
  sagaMiddleware.run(rootSaga);
  return store;
}