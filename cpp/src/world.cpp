/* Copyright (c) 2022 Pixel Flux
 *
 * Permission is hereby granted, free of charge, to any person obtaining
 * a copy of this software and associated documentation files (the
 * "Software"), to deal in the Software without restriction, including
 * without limitation the rights to use, copy, modify, merge, publish,
 * distribute, sublicense, and/or sell copies of the Software, and to
 * permit persons to whom the Software is furnished to do so, subject to
 * the following conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
 * IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
 * CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
 * TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
 * SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */

#include "world.hpp"

#include <stdexcept>

using namespace pyflecs;

world::world() : 
    mpRaw(ecs_init())
{

}

world::~world()
{
    ecs_fini(mpRaw);
}

pyflecs::entity world::entity()
{
    return pyflecs::entity(mpRaw, ecs_new_id(mpRaw));
}

pyflecs::entity world::entity(std::string name)
{
    ecs_entity_desc_t desc{};
    desc.name = name.c_str();
    ecs_entity_init(mpRaw, &desc);
    return pyflecs::entity(mpRaw, ecs_entity_init(mpRaw, &desc));
}

pyflecs::entity world::entity(pyflecs::entity &c)
{
    return pyflecs::entity(mpRaw, ecs_new_w_id(mpRaw, c.raw()));
}

std::vector<pyflecs::entity> world::bulk_entity_w_id(ecs_id_t eid, 
    int32_t count)
{
    auto result = ecs_bulk_new_w_id(mpRaw, eid, count);
    if (result == nullptr)
        throw std::runtime_error("Error on bulk creation with ID");
    std::vector<pyflecs::entity> entities;
    for (int32_t idx = 0; idx < count; idx++)
    {
        entities.push_back(pyflecs::entity(mpRaw, result[idx]));
    }
    return entities;
}

pyflecs::bulk_entity_builder world::bulk_entity_builder(int32_t count)
{
    return pyflecs::bulk_entity_builder(mpRaw, count);
}

pyflecs::entity world::lookup(std::string name)
{
    return pyflecs::entity(mpRaw, ecs_lookup(mpRaw, name.c_str()));
}

pyflecs::entity world::lookup_path(std::string name)
{
    return pyflecs::entity(mpRaw, ecs_lookup_path(mpRaw, 0, name.c_str()));
}

pyflecs::id world::lookup_by_id(ecs_id_t eid)
{
    return pyflecs::id(mpRaw, eid);
}

pyflecs::entity world::component(std::string name, size_t size, 
    size_t alignment)
{
    ecs_component_desc_t desc = { 0 };
    desc.entity.entity = 0;
    desc.entity.name = name.c_str();
    desc.entity.symbol = name.c_str();
    desc.size = size;
    desc.alignment = alignment;
    auto component_id = ecs_component_init(mpRaw, &desc);
    if (component_id == 0)
        throw std::runtime_error("Component could not be created");
    return pyflecs::entity(mpRaw, component_id);
}

pyflecs::filter world::create_filter(std::string name, 
    std::string expr, bool instanced, std::vector<ecs_term_t> terms)
{
    ecs_filter_t f;
    ecs_filter_desc_t desc{};
    desc.name = name.c_str();
    desc.expr = expr.c_str();
    desc.instanced = instanced;

    if (terms.size() > ECS_TERM_DESC_CACHE_SIZE)
    {
        // TODO
    }
    else
    {
        for (auto idx = 0; idx < terms.size(); idx++)
        {
            desc.terms[idx] = terms[idx];
        }
    }    
    auto result = ecs_filter_init(mpRaw, &f, &desc);
    if (result != 0)
    {
        throw std::runtime_error("Filter creation failed.");
    }

    return pyflecs::filter(mpRaw, f);
}

pyflecs::query world::create_query(std::string name,
    std::string expr, bool instanced, std::vector<ecs_term_t> terms)
{
    ecs_query_desc_t desc{};
    desc.filter.name = name.c_str();
    desc.filter.expr = expr.c_str();
    desc.filter.instanced = instanced;

    if (terms.size() > ECS_TERM_DESC_CACHE_SIZE)
    {
        // TODO
    }
    else
    {
        for (auto idx = 0; idx < terms.size(); idx++)
        {
            desc.filter.terms[idx] = terms[idx];
        }
    }    
    auto q = ecs_query_init(mpRaw, &desc);
    if (q == nullptr)
    {
        throw std::runtime_error("Query creation failed.");
    }
    return pyflecs::query(mpRaw, q);
}