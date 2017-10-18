import {createStore, applyMiddleware, compose} from 'redux'
import createSagaMiddleware from 'redux-saga'

export function configureStore() {
  const sagaMiddleware = createSagaMiddleware();
  return createStore(
    
    compose(
      window.__REDUX_DEVTOOLS_EXTENSION__ && window.__REDUX_DEVTOOLS_EXTENSION__(),
      applyMiddleware(sagaMiddleware)
    )
  );
}