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

pyflecs::entity world::lookup(std::string name)
{
    return pyflecs::entity(mpRaw, ecs_lookup(mpRaw, name.c_str()));
}

pyflecs::entity world::lookup_path(std::string name)
{
    return pyflecs::entity(mpRaw, ecs_lookup_path(mpRaw, 0, name.c_str()));
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
    std::string expr, std::vector<pyflecs::entity> terms)
{
    ecs_filter_t f;
    ecs_filter_desc_t desc{};
    desc.name = name.c_str();
    desc.expr = expr.c_str();

    if (terms.size() > ECS_TERM_DESC_CACHE_SIZE)
    {
        // TODO
    }
    else
    {
        for (auto idx = 0; idx < terms.size(); idx++)
        {
            desc.terms[idx] = ecs_term_t{ terms[idx].raw() };
        }
    }    ecs_filter_init(mpRaw, &f, &desc);

    return pyflecs::filter(mpRaw, f);
}