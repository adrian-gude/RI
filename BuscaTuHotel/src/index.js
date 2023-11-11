import React from 'react';
import ReactDOM from 'react-dom';
import {
	ReactiveBase,
	DataSearch,
	ReactiveList,
  RatingsFilter,
  MultiRange,
  MultiDropdownList,
  RangeInput,
  ResultList,
} from '@appbaseio/reactivesearch';
import './index.css';

import StarIcon from '@mui/icons-material/Star';
import CircleIcon from '@mui/icons-material/Circle';
import Rating from '@mui/material/Rating';

/*TODO: (PENDIENTE)
 - mejorar listado resultados:
    - poner servicios como tags
    - hacer coincidir los colores de los componentes: slider, puntuación y paginación
    - centrar bien las imágenes
 - hacer que las abreviaturas de la paginación estén en español
 - selección de idiomas y servicios funciona como un OR y debería ser un AND
*/

class Main extends React.Component {
  render() {
    return (
      <ReactiveBase
        app="hotels" // Nombre de tu aplicación de Elasticsearch
        url="http://localhost:9200" // URL de tu instancia de Elasticsearch
      >
        <div className='text-align-center'>
          <div className='header'>
              <h1>Busca tu Hotel</h1>
          </div>
        </div>
        
        <div style={{ display: 'flex', flexDirection: 'row'}} className='colorFondoPrincipal'>
          <div
            style={{
              display: 'flex',
              flexDirection: 'column',
              width: '24%',
              margin: '10px',
              marginTop: '2%',
            }}
          >
            <div style={{marginBottom:'5%'}}>
              <MultiDropdownList
                componentId="comunidad_multidropselector"
                compoundClause="filter"
                dataField="comunidad"
                title="Comunidades autónomas"
                sortBy="asc"
                showCount={true}
                placeholder="Comunidades"
                showFilter={true}  
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }} 
              />
            </div>
            <div style={{marginBottom:'5%'}}>
              <RangeInput
                componentId="precio_slider_input"
                dataField="precio"
                title="Precio"
                range={{
                  start: 0,
                  end: 1500,
                }}
                defaultValue={{
                  start: 50,
                  end: 800,
                }}
                rangeLabels={{
                  start: '0',
                  end: '1500',
                }}
                showHistogram={false}
                showFilter={true}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }}
              />
            </div>
            <div style={{marginBottom:'5%'}}>
              <RatingsFilter
                componentId="puntuacion_ratingselector"
                dataField="puntuacion"
                title="Valoración"
                icon={<CircleIcon htmlColor="seagreen  " />}
                dimmedIcon={<CircleIcon htmlColor='grey'/>}
                data={[
                  { start: 1, end: 5, label: '1 o más' },
                  { start: 2, end: 5, label: '2 o más' },
                  { start: 3, end: 5, label: '3 o más' },
                  { start: 4, end: 5, label: '4 o más' },
                  { start: 5, end: 5, label: '5' }
                ]}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }}
              />
            </div>
            <div style={{marginBottom:'5%'}}>
              <MultiRange
                componentId="categoria_multiselector"
                compoundClause="filter"
                dataField="categoria"
                data={[
                  //{ start: 1, end: 1, label: <StarIcon htmlColor="#F2B203"/> },
                  { start: 1, end: 1, label: '1 estrella' },
                  { start: 2, end: 2, label: '2 estrellas' },
                  { start: 3, end: 3, label: '3 estrellas'  },
                  { start: 4, end: 4, label: '4 estrellas'  },
                  { start: 5, end: 5, label: '5 estrellas'  },
                  //{ start: 5, end: 5, label: <Rating name="read-only" value={5} readOnly /> },
                ]}
                title="Categoría"
                showCheckbox={true}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }}
              />
            </div>
            <div style={{marginBottom:'5%'}}>
              <MultiDropdownList
                componentId="idiomas_multidropselector"
                compoundClause="filter"
                dataField="idiomas"
                title="Idiomas"
                //size={100}
                sortBy="count"
                showCount={true}
                placeholder="Idiomas"
                showFilter={true}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }} 
              />
            </div>
            <div style={{marginBottom:'5%'}}>
              <MultiDropdownList
                componentId="servicios_multidropselector"
                compoundClause="filter"
                dataField="servicios"
                title="Servicios"
                //size={100}
                sortBy="count"
                showCount={true}
                placeholder="Servicios"
                showFilter={true}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }}  
              />
            </div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', width: '72%', marginLeft: '1.4%' }}>
            <div style={{ marginTop: '2%' }}>
              <DataSearch
                componentId="searchbox"
                dataField={[
                  {
                    field: 'nombre',
                    weight: 3,
                  },
                  {
                    field: 'localizacion',
                    weight: 1,
                  }
                ]}
                placeholder="Busca un hotel"
                autosuggest={true}
                //enableRecentSuggestions={true}
                //enablePopularSuggestions={true}
                //enablePredictiveSuggestions={true}
                react={{
                  and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                  'idiomas_multidropselector', 'servicios_multidropselector'],
                }}
              />
            </div>
            <ReactiveList
              componentId="results"
              dataField="_score"
              size={15}
              //sortBy='desc'
              sortOptions={[
                {
                  label: "-", //Ordenación por defecto, que es por la puntuación
                  dataField: "_score",
                  sortBy: "desc"
                },
                {
                  label: "Puntuación descendente", //Ordenación por la puntuación del hotel de forma descendente
                  dataField: "puntuacion",
                  sortBy: "desc"
                },
                {
                  label: "Puntuación ascendente", //Ordenación por la puntuación del hotel de forma ascendente
                  dataField: "puntuacion",
                  sortBy: "asc"
                }
              ]}
              defaultSortOption='-'
              stream={true}
              pagination={true}
              paginationAt='bottom'
              react={{
                and: ['searchbox', 'comunidad_multidropselector', 'categoria_multiselector', 'precio_slider_input', 'puntuacion_ratingselector',
                 'idiomas_multidropselector', 'servicios_multidropselector'],
              }}
              loader={<div>Cargando...</div>}
              showResultStats={true} //Mostrar estadísticas de resultados
              render={({ data }) => (
                <ReactiveList.ResultListWrapper>
                  {data.map(item => (
                    <div className='hotelWrapper'>
                      <ResultList key={item._id}>
                        <div className='column-img'>
                          <img src={item.imageUrl} className='result-image'/>
                        </div>
                        <div className='column'>
                        <ResultList.Content>
                          <ResultList.Title>
                            <div className='grid-container'>
                              <div className='column hotelNameText'>
                                <a href={item.url} target="_blank" rel="noopener noreferrer" className="no-link-style">
                                  <div dangerouslySetInnerHTML={{ __html: item.nombre }} />
                                </a>
                              </div>
                              <div className='column priceText'>
                                <span>
                                      {item.precio}€
                                </span>
                              </div>
                            </div>
                          </ResultList.Title>
                          <ResultList.Description>
                            <div className='grid-container'>
                              <div className='grid-container row'>
                                <div className='column'>
                                  <span>
                                    <Rating name="read-only" value={item.categoria} readOnly />
                                  </span>
                                </div>
                                <div className='column text-align-end'>
                                  <span>
                                    {item.puntuacion} - {item.n_opiniones} opiniones
                                  </span>
                                </div>
                              </div>
                            </div>
                            <div className='row'>
                                <span>
                                  {item.comunidad} - {item.localizacion}
                                </span>
                            </div>
                            <div className='row'>
                                <span>
                                  {item.servicios}
                                </span>
                            </div>
                          </ResultList.Description>
                        </ResultList.Content>
                        </div>
                      </ResultList>
                    </div>
                  ))}
                </ReactiveList.ResultListWrapper>
              )}
              renderResultStats={ //Definir estadísticas personalizadas de resultados
                function(stats){
                    return (
                        `Mostrando ${stats.displayedResults} de un total de ${stats.numberOfResults} encontrados en ${stats.time} ms`
                    )
                }
            }
            />
          </div>
          
        </div>
        
      </ReactiveBase>

    );
  }
}

ReactDOM.render(<Main />, document.getElementById('root'));


//TODO: (PENDIENTE)
/*
- Permitir elegir al usuario el nº de elementos por página a mostrar
- Mejorar el diseño de la página (estilo, colores, etc.)
- Definir visualización correcta de cada hotel del listado
- Intentar incluír un mapa con el nº de hoteles por comunidad
- Hacer el ordenacimiento del listado, actualmente no funciona
- Hacer que si pinchas en un hotel te lleve a su página web (haciendo uso del campo 'url)
- Verificar correcto funcionamiento de los componentes, en especial el buscador
- Comprobar que el diseño es responsive
*/



